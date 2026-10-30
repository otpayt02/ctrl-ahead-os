#!/usr/bin/env python3
"""Script FIRST, render manifest SECOND, from the same timestamps.
Usage: python3 make_script_and_manifest.py --topic "Nemotron 3.5 Bolt on a 24GB card" --subniche "Local LLM setups" --week 2026-W43 --out-dir data/portfolio/2026-W43/003-example
Input evidence: week_intelligence.json (optional) — every factual claim in the script
must cite an evidence URL from it, or be marked UNVERIFIED in the script itself.
Output: script.md (timestamped segments, VO text placeholders — NOT a voiceover file)
        render_manifest.json (one visual per segment, label + source file, duration from segment)
Visual labels allowed: live | fetched render | screen record | livestream frame | NOT RUN | AI
No VO is generated here. VO/render stay HELD until Oliver approves script.md in chat.
"""
import argparse, json, os
SEGMENTS=[
 ("00:00","00:30","Hook","What the topic is, in one sentence, and why this week matters"),
 ("00:30","02:00","Evidence","The dated changelog / release / repo evidence, with links"),
 ("02:00","04:00","Live test","Oliver's artifact: what was actually tried, what ran, what did NOT run"),
 ("04:00","05:30","What breaks / what to watch","Limits, costs, quota, VRAM, or deprecation — the honest catch"),
 ("05:30","06:00","Close + next step","One concrete thing the viewer can do, and the next video's topic (only if approved)"),
]
def to_sec(t):
    m,s=map(int,t.split(":")); return m*60+s
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--topic", required=True); ap.add_argument("--subniche", required=True)
    ap.add_argument("--week", required=True); ap.add_argument("--evidence", default=""); ap.add_argument("--out-dir", required=True); a=ap.parse_args()
    ev={}
    if a.evidence and os.path.exists(a.evidence): ev=json.load(open(a.evidence))
    os.makedirs(a.out_dir, exist_ok=True)
    lines=[f"# Script — {a.topic}", f"Subniche: {a.subniche} | Week: {a.week} | Status: DRAFT — NOT APPROVED, VO/render HELD", "",
           "Every factual claim below must have an evidence link, or be marked UNVERIFIED. Do not read a claim as proven if its link is missing.", ""]
    manifest={"topic":a.topic,"subniche":a.subniche,"week":a.week,"status":"DRAFT — script not approved, render HELD","segments":[]}
    for start,end,title,note in SEGMENTS:
        dur=to_sec(end)-to_sec(start)
        lines.append(f"## {start}-{end} — {title} ({dur}s)")
        lines.append(f"VO draft (to be approved, not yet recorded): [{note} — write the actual script text here, with evidence links.]")
        lines.append("")
        manifest["segments"].append({"start":start,"end":end,"duration_s":dur,"title":title,"vo_note":note,
            "visual":{"label":"NOT RUN","source_file":"","note":"Replace with a reviewed capture: live / fetched render / screen record / livestream frame, with its file path, before rendering."}})
    open(os.path.join(a.out_dir,"script.md"),"w").write("\n".join(lines))
    json.dump(manifest, open(os.path.join(a.out_dir,"render_manifest.json"),"w"), indent=2)
    print(f"wrote {a.out_dir}/script.md and render_manifest.json — {len(SEGMENTS)} segments, total {to_sec('06:00')}s planned (not a VO duration)")
if __name__=="__main__": main()
