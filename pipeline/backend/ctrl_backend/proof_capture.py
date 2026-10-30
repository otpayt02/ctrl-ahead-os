"""Proof capture specs for Muse's browser feature. The backend cannot drive the live
browser itself; it SPECS each capture task (screenshot / screen record) with the exact
target and the mouthfeed treatment, and the parent agent executes them via browser tools.
Only topics with a real evidence/artifact target get a task — no target, no fake proof."""

def spec_tasks(db, run_id, chosen, angles):
    tasks = []
    targets = []
    if chosen:
        lane, top = chosen
        targets.append((f"{top['title']} ({lane})", top["video_id"], "reference_video"))
    for a in angles[:5]:
        if a["kind"] in ("github_repo", "drive_file"):
            targets.append((a["topic"], a["source_ref"], "artifact"))
    for topic, target, kind in targets:
        is_url = str(target).startswith("http")
        task = {"topic": topic, "kind": "screenshot" if kind != "reference_video" else "screen_record",
                "target": target if is_url else f"https://www.youtube.com/watch?v={target}",
                "instruction": ("Capture with Muse's browser: open the target, take a screenshot (and a short "
                                "screen recording if motion matters). In the render, show it FULL-SCREEN, "
                                "zoomed 1.35x with smooth pan lined up to narration, cited text highlighted "
                                "large as spoken (mouthfeed rule). If the browser cannot export a true "
                                "screenshot, use its best in-system capture and record that limitation in "
                                "the render manifest — never label a render as a live screenshot."),
                "status": "specced"}
        db.execute("INSERT INTO proof_tasks(run_id,topic,kind,target,instruction,status) VALUES(?,?,?,?,?,?)",
                   (run_id, task["topic"], task["kind"], task["target"], task["instruction"], "specced"))
        tasks.append(task)
    db.commit()
    return tasks
