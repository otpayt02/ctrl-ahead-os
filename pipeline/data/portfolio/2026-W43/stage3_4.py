import json, pathlib, statistics, collections
base = pathlib.Path.home()/"workspace/goals/ctrl-ahead-os-ai-video/files/pipeline/data/portfolio/2026-W43/stage_narrowing"
s1=json.load(open(base/"stage1_general_2026-10-26.json"))
s2=json.load(open(base/"stage2_references_2026-10-26.json"))
# Stage 3 manifests per lane, from reference metadata
manifests={}
for lane, d in s2["lanes"].items():
    shorts=d["refs_shorts_5"]; longs=d["refs_longs_5"]
    allrefs=shorts+longs
    dur_long=[v["duration_s"] for v in longs]; dur_short=[v["duration_s"] for v in shorts]
    manifests[lane]={
      "refs": {"shorts": len(shorts), "longs": len(longs), "short_titles": [v["title"] for v in shorts], "long_titles": [v["title"] for v in longs]},
      "duration_bands": {"shorts_s": dur_short, "longs_s": dur_long, "long_median_s": statistics.median(dur_long) if dur_long else None},
      "title_patterns": "Caps / update / vs / breakdown / tutorial — taken from reference titles, not from watching full videos",
      "hook_pattern": "First line names a dated change or a test result, then a verdict promise — pattern from titles, to be confirmed by watching before a final render",
      "segment_cadence": "Long: hook 0-30s, evidence beats in 60-120s blocks, verdict/checklist close. Short: one claim, one proof beat, one close, under 60s.",
      "visual_system_boilerplate": "Dark grid, one headline per claim, pill label, word-pop captions, slow zoom, proof card zoom/pan on evidence beats — this is the existing Ctrl-Ahead boilerplate, not a claim that every reference uses it",
      "source": "Metadata-derived (title, duration, velocity, channel) from YouTube API 2026-10-26, 7d window. NOT a frame-by-frame watch of all 50 references.",
      "gap": "Shorts count below 5 where the 7d pool had fewer than 5 videos under 60s — not padded."
    }
# Stage 4: chosen lane = Model comparisons, channels/outliers
chosen="Model comparisons"
d=s2["lanes"][chosen]
allv=[]
for kind in ("general","shorts_search"):
    allv.extend(d[kind])
uniq={v["id"]:v for v in allv}; allv=list(uniq.values())
med=statistics.median([v["velocity"] for v in allv]) if allv else 0
outliers=[v for v in allv if v["velocity"]>3*med]
chan=collections.Counter(v["channel"] for v in allv)
stage4={"chosen_lane":chosen,"reason":"Highest lane relevance + artifact fit after outlier correction: median 670 in stage1, top video is the 005 source itself, plus open-model and Claude Duet breakdowns. Interviews/podcasts and predictions were excluded — their medians were driven by BBC, podcast and drama outliers, not by buildable AI-niche videos. Faceless systems excluded as pipeline-as-topic.","pool":len(allv),"median_velocity":round(med,2),"outliers_gt_3x_median":[{"title":v["title"],"channel":v["channel"],"velocity":v["velocity"],"views":v["views"]} for v in sorted(outliers, key=lambda x:-x["velocity"])[:10]],"top_channels":chan.most_common(10),"top_videos":[{"title":v["title"],"channel":v["channel"],"velocity":v["velocity"],"duration_s":v["duration_s"]} for v in sorted(allv, key=lambda x:-x["velocity"])[:10]}
json.dump({"stage3_manifests":manifests,"stage4_chosen":stage4}, open(base/"stage3_4_manifests_2026-10-26.json","w"), indent=1)
print("chosen:", chosen, "pool", len(allv), "median", round(med,2), "outliers", len(outliers))
print("top channels:", chan.most_common(5))
