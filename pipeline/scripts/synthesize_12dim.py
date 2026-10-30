#!/usr/bin/env python3
"""12-dim synthesis from EVIDENCE ONLY.
Inputs: --github github.json, --changelogs changelogs.json, --youtube script_inputs.json (optional, existing partial is OK)
Output: week_intelligence.json with 12 dimensions per lane.
Rule: a dimension lists only items with evidence. If <10, count is <10 and coverage=PARTIAL.
Never pad, never invent a creator, repo, or changelog entry.
Inference score (see README): changelog 25 + github percentile 25 + youtube percentile 25 + artifact 15 + buildability 10.
Artifact/buildability default to 0/UNVERIFIED unless the user supplies --artifact-fit json.
"""
import argparse, json, os, datetime
def load(p):
    return json.load(open(p)) if p and os.path.exists(p) else {}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--github", default=""); ap.add_argument("--changelogs", default="")
    ap.add_argument("--youtube", default=""); ap.add_argument("--subniche", default="AI tool reviews")
    ap.add_argument("--cluster", default="tools"); ap.add_argument("--week", default="")
    ap.add_argument("--out", required=True); a=ap.parse_args()
    gh=load(a.github); ch=load(a.changelogs); yt=load(a.youtube)
    week=a.week or f"{datetime.date.today().isocalendar()[0]}-W{datetime.date.today().isocalendar()[1]:02d}"
    repos=gh.get("repos", [])[:10]
    companies=[]
    for c in ch.get("companies", []):
        for s in c.get("sources", []):
            for it in s.get("items", [])[:10]:
                if isinstance(it, dict) and "title" in it: companies.append({"company":c["company"],"title":it["title"],"url":it.get("url","")})
    yt_videos=[]
    # Real script_inputs.json shape: {"lanes": {lane_name: [video, ...], ...}, ...}
    # Also handle lane->list directly. Never assume a flat list.
    lanes_map = yt.get("lanes") if isinstance(yt, dict) else None
    if isinstance(lanes_map, dict):
        for lane, vids in lanes_map.items():
            if isinstance(vids, list): yt_videos.extend(vids[:10])
    elif isinstance(yt, dict):
        for lane, vids in yt.items():
            if isinstance(vids, list): yt_videos.extend(vids[:10])
    dims={
      "01_top10_creators_to_listen": {"items": [], "coverage": "UNVERIFIED", "note": "Creators require channel evidence from scored snapshots — not derived here, do not use as a top-10 claim."},
      "02_top10_outlier_videos": {"items": [], "coverage": "UNVERIFIED", "note": "Outlier ratio needs >=3 channel videos in DB — not computed here."},
      "03_top10_best_videos_past_week": {"items": yt_videos[:10], "coverage": "PARTIAL" if yt_videos else "UNVERIFIED"},
      "05_top10_incumbent_changelogs": {"items": companies[:10], "coverage": "PARTIAL" if companies else "UNVERIFIED"},
      "09_top10_trending_github_repos": {"items": [{"full_name":r["full_name"],"url":r["url"],"stars":r["stars"],"stars_7d":r.get("stars_7d")} for r in repos], "coverage": "PARTIAL" if repos else "UNVERIFIED"},
    }
    # Fill remaining dims explicitly as UNVERIFIED, not empty-by-accident
    for k in ["04_top10_best_channels_growth","06_top10_rising_companies","07_top10_industry_watchouts","08_top10_search_queries","10_top10_production_tools","11_top10_diy_builds","12_top10_workflows_and_reasons"]:
        dims[k]={"items": [], "coverage": "UNVERIFIED", "note": "No evidence in this run's inputs — left empty, not padded."}
    out={"week_window": week, "subniche": a.subniche, "cluster": a.cluster,
         "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
         "dimensions": dims,
         "inference_note": "Score only computed in make_script_and_manifest.py once a topic + artifact fit are chosen. This file is evidence, not a ranking."}
    os.makedirs(os.path.dirname(a.out), exist_ok=True); json.dump(out, open(a.out,"w"), indent=2)
    print(f"wrote {a.out}: github {len(repos)}, changelogs {len(companies)}, youtube {len(yt_videos)}")
if __name__=="__main__": main()
