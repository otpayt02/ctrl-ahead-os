import json, pathlib, statistics, collections
base = pathlib.Path.home()/"workspace/goals/ctrl-ahead-os-ai-video/files/pipeline/data/portfolio/2026-W43/stage_narrowing"
s2=json.load(open(base/"stage2_references_2026-10-26.json"))
manifests={}
for lane, d in s2["lanes"].items():
    shorts=d["refs_shorts_5"]; longs=d["refs_longs_5"]
    manifests[lane]={
        "refs": {"shorts": len(shorts), "longs": len(longs), "short_titles": [v["title"] for v in shorts], "long_titles": [v["title"] for v in longs]},
        "long_median_s": statistics.median([v["duration_s"] for v in longs]) if longs else None,
        "hook_pattern": "First line names a dated change or a test result, then a verdict promise - from titles, to be confirmed by watching before a final render",
        "segment_cadence": "Long: hook 0-30s, evidence beats in 60-120s blocks, verdict/checklist close. Short: one claim, one proof beat, one close, under 60s.",
        "visual_system_boilerplate": "Dark grid, one headline per claim, pill label, word-pop captions, slow zoom, proof card zoom/pan on evidence beats - existing Ctrl-Ahead boilerplate, not a claim every reference uses it",
        "source": "Metadata-derived (title, duration, velocity, channel) from YouTube API 2026-10-26, 7d window. NOT a frame-by-frame watch of all references.",
        "gap": "Shorts below 5 where the 7d pool had fewer than 5 videos under 60s - not padded.",
    }
chosen="Model comparisons"
d=s2["lanes"][chosen]
allv=list({v["id"]: v for v in d["general"]+d["shorts_search"]}.values())
med=statistics.median([v["velocity"] for v in allv])
outliers=[v for v in allv if v["velocity"]>3*med]
chan=collections.Counter(v["channel"] for v in allv)
outlier_list=[]
for v in sorted(outliers, key=lambda x: -x["velocity"])[:10]:
    outlier_list.append({"title": v["title"], "channel": v["channel"], "velocity": v["velocity"], "views": v["views"]})
top_list=[]
for v in sorted(allv, key=lambda x: -x["velocity"])[:10]:
    top_list.append({"title": v["title"], "channel": v["channel"], "velocity": v["velocity"], "duration_s": v["duration_s"]})
stage4={
    "chosen_lane": chosen,
    "reason": "Highest relevance + artifact fit after outlier correction: median 670 in stage1, top video is the 005 source, plus open-model and Claude Duet breakdowns. Interviews/podcasts and predictions excluded - medians driven by BBC, podcast and drama outliers. Faceless systems excluded as pipeline-as-topic. AI video generation pool is polluted by non-English drama in stage2, so it is weaker than its stage1 median suggested.",
    "pool": len(allv),
    "median_velocity": round(med, 2),
    "outliers_gt_3x_median": outlier_list,
    "top_channels": chan.most_common(10),
    "top_videos": top_list,
}
json.dump({"stage3_manifests": manifests, "stage4_chosen": stage4}, open(base/"stage3_4_manifests_2026-10-26.json","w"), indent=1)
print("chosen pool", len(allv), "median", round(med,2), "outliers", len(outliers), "channels", chan.most_common(5))
