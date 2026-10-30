#!/usr/bin/env python3
"""Ctrl-Ahead OS backend orchestrator — one entrypoint.

Chain: harvest (live API if YT_API_KEY else proxy_existing) -> velocity score ->
stage narrowing (niche -> 35 subniches -> per-lane top-100/top-10 -> chosen lane) ->
Brain index (local + Drive + GitHub) -> angles -> Grill Me import/queue ->
script draft + render manifest -> proof-capture specs -> render queue handoff.

Usage:
  python3 run_pipeline.py [--mode auto|live|proxy] [--per-lane 50] [--skip-brain-connectors]
Output: runs/<YYYY-MM-DD-HHMM>-<mode>/ with run_manifest.json/.md, top100.json,
script_inputs/<lane>.json, angles.json, render_queue.json, proof_capture_tasks.json,
grill_queue_snapshot.json, plus the chosen topic's script.md + render_manifest.json.
Honesty rule: the run manifest states mode, lanes covered, videos scored, and
PARTIAL vs FULL coverage. Nothing is padded, no velocity/CTR is invented.
Gate: render queue status = queued_manifest_gate (Gate 1, Oliver approves the full
render manifest before publish). No publishing happens here, ever."""
import argparse, datetime, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from ctrl_backend import config, db as dbmod, harvest as hv, mining, scoring, brain, grillme, scriptgen, proof_capture

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["auto", "live", "proxy"], default="auto")
    ap.add_argument("--per-lane", type=int, default=50)
    ap.add_argument("--skip-brain-connectors", action="store_true",
                    help="index local files only (skip Drive/GitHub connector calls)")
    a = ap.parse_args()

    mode = a.mode
    if mode == "auto":
        mode = "live" if config.yt_api_key() else "proxy"
    run_id = datetime.datetime.now().strftime("%Y-%m-%d-%H%M") + f"-{mode}"
    run_dir = config.RUNS_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    week = config.week_window()
    db = dbmod.connect()
    lanes = hv.load_lanes()
    notes = []
    db.execute("INSERT OR REPLACE INTO pipeline_runs(run_id,started_at,mode,week_window) VALUES(?,?,?,?)",
               (run_id, datetime.datetime.now(datetime.timezone.utc).isoformat(), mode, week))
    db.commit()

    # CP-harvest
    if mode == "live":
        try:
            scored, searches = hv.harvest_live(db, lanes, per_lane_limit=a.per_lane)
            harvest_detail = f"live API harvest, searches used today: {searches}"
            coverage = "PARTIAL" if scored < len(lanes) * 10 else "FULL"
        except hv.QuotaStop as e:
            scored, harvest_detail, coverage = 0, f"QUOTA STOP: {e}", "PARTIAL"
            notes.append("Quota stop hit — no same-day retry (pipeline rule). Re-run tomorrow or in proxy mode.")
    else:
        scored, lanes_with, detail = hv.harvest_proxy_existing(db)
        harvest_detail = f"proxy_existing: {detail}"
        coverage = "PARTIAL"
        notes.append("No YT_API_KEY in env — NO new YouTube harvest ran. Numbers below come from the "
                     "previous real harvest already on disk (2026-W43, itself PARTIAL: 15 lanes, 88 searches then 429).")
    lanes_covered = db.execute("SELECT COUNT(DISTINCT lane) c FROM videos").fetchone()["c"]

    # mining (live only; proxy reuses stored hooks/comments)
    mining_detail = "proxy: reused hooks/comments stored in existing bundles"
    if mode == "live" and scored:
        per_lane_tmp, _ = scoring.narrow(db, lanes)
        top_ids = {lane: [r["video_id"] for r in rows] for lane, rows in per_lane_tmp.items()}
        mined, calls, st = mining.mine_live(db, top_ids)
        ok, tst = mining.transcripts_for(db, [v for rows in top_ids.values() for v in rows[:1]][:20])
        mining_detail = f"live: {mined} comments in {calls} calls ({st}); transcripts ok={ok} ({tst})"

    # score + narrow
    per_lane, chosen = scoring.narrow(db, lanes)
    (run_dir / "top100.json").write_text(json.dumps(
        {lane: [dict(r) for r in rows] for lane, rows in per_lane.items()}, indent=1, default=str))
    si_dir = run_dir / "script_inputs"
    si_dir.mkdir(exist_ok=True)
    for lane, rows in per_lane.items():
        payload = {"subniche": lane, "cluster": lanes[lane]["cluster"], "mode": mode, "week": week,
                   "coverage": coverage, "top10": [
                       {"video_id": r["video_id"], "title": r["title"], "channel": r["channel"],
                        "views": r["views"], "velocity_views_per_hour": r["velocity"],
                        "published_at": r["published_at"],
                        "evidence_url": f"https://www.youtube.com/watch?v={r['video_id']}"}
                       for r in rows[:config.SCRIPT_INPUTS_TOP_N]]}
        slug = lane.lower().replace(" ", "-").replace("/", "-").replace("&", "and")
        (si_dir / f"{slug}.json").write_text(json.dumps(payload, indent=1, default=str))

    # brain
    n_local, _ = brain.index_local(db)
    brain_detail = {"local_files": n_local}
    if not a.skip_brain_connectors:
        n_drive, drive_st = brain.index_drive(db)
        n_gh, gh_st = brain.index_github(db)
        brain_detail.update({"drive_files": n_drive, "drive_status": drive_st,
                             "github_repos": n_gh, "github_status": gh_st})
    topics_for_angles = [(lane, rows[0]["title"]) for lane, rows in per_lane.items() if rows]
    angles = brain.propose_angles(db, run_id, topics_for_angles)
    (run_dir / "angles.json").write_text(json.dumps(angles, indent=1))

    # grill me
    imported, checked = grillme.import_exports()
    approved_grill = grillme.approved_concepts()
    (run_dir / "grill_queue_snapshot.json").write_text(json.dumps(
        {"imported_this_run": imported, "sources_checked": checked,
         "queue": grillme.load_queue(), "approved": approved_grill}, indent=1))

    # script + manifest + render queue (chosen automate pick + approved grill concepts)
    queue = []
    def enqueue(topic, lane, evidence_url, angle, origin):
        s_path, m_path = scriptgen.build(run_dir / "drafts" / (origin + "-" + lane.lower().replace(" ", "-").replace("/", "-")),
                                         topic, lane, week, evidence_url, angle, origin)
        db.execute("INSERT INTO render_queue(run_id,topic,lane,origin,script_path,manifest_path,status,created_at)"
                   " VALUES(?,?,?,?,?,?,?,?)",
                   (run_id, topic, lane, origin, s_path, m_path, "queued_manifest_gate",
                    datetime.datetime.now(datetime.timezone.utc).isoformat()))
        queue.append({"topic": topic, "lane": lane, "origin": origin, "script": s_path,
                      "render_manifest": m_path, "status": "queued_manifest_gate"})
    if chosen:
        lane, top = chosen
        ang = next((x for x in angles if x["topic"] == top["title"]), None)
        fit = 15 if ang else 7
        vel_values = [r["velocity"] or 0 for r in per_lane[lane]]
        pct = scoring.percentile(vel_values, top["velocity"] or 0)
        score = scoring.topic_score(pct, fit)
        db.execute("INSERT INTO topics_scored(run_id,lane,topic,score,youtube_percentile,artifact_fit,buildability,evidence_sources,status)"
                   " VALUES(?,?,?,?,?,?,?,?,?)", (run_id, lane, top["title"], score, pct, fit, 10, 2 if ang else 1,
                                                 "automate-pick" if ang else "single-source"))
        enqueue(top["title"], lane, f"https://www.youtube.com/watch?v={top['video_id']}", ang, "automate")
    for g in approved_grill:
        enqueue(g["concept"], g.get("subniche", ""), "", None, "grill_me")
    db.commit()
    (run_dir / "render_queue.json").write_text(json.dumps(queue, indent=1))

    # proof capture specs
    tasks = proof_capture.spec_tasks(db, run_id, chosen, angles)
    (run_dir / "proof_capture_tasks.json").write_text(json.dumps(tasks, indent=1))

    finished = datetime.datetime.now(datetime.timezone.utc).isoformat()
    db.execute("UPDATE pipeline_runs SET lanes_covered=?, videos_scored=?, coverage=?, notes=?, finished_at=? WHERE run_id=?",
               (lanes_covered, scored, coverage, " | ".join(notes), finished, run_id))
    db.commit()
    manifest = {"run_id": run_id, "mode": mode, "week": week, "coverage": coverage,
                "lanes_in_config": len(lanes), "lanes_with_videos": lanes_covered,
                "videos_scored": scored, "harvest": harvest_detail, "mining": mining_detail,
                "brain": brain_detail, "angles_proposed": len(angles),
                "grill_me": {"imported": imported, "approved_concepts": len(approved_grill)},
                "chosen_lane": chosen[0] if chosen else None,
                "chosen_topic": chosen[1]["title"] if chosen else None,
                "render_queue": queue, "proof_tasks_specced": len(tasks), "notes": notes,
                "gates": "Render queue is queued_manifest_gate — Gate 1 (Oliver approves full render manifest) before publish. Hands-free covers everything before that."}
    (run_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=1, default=str))
    md = [f"# Run {run_id}", f"Mode: {mode} | Week: {week} | Coverage: **{coverage}**",
          f"Lanes in config: {len(lanes)} | Lanes with videos: {lanes_covered} | Videos scored: {scored}",
          f"Harvest: {harvest_detail}", f"Mining: {mining_detail}", f"Brain: {brain_detail}",
          f"Angles proposed: {len(angles)} | Grill Me imported: {imported}, approved: {len(approved_grill)}",
          f"Chosen: {manifest['chosen_topic']} ({manifest['chosen_lane']})",
          f"Proof tasks specced: {len(tasks)}", "", "## Notes"] + [f"- {n}" for n in notes]
    (run_dir / "run_manifest.md").write_text("\n".join(md))
    print(json.dumps(manifest, indent=1, default=str))

if __name__ == "__main__":
    main()
