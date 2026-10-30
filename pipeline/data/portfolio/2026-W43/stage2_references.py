import json, sys, datetime as dt, pathlib, re
sys.path.insert(0, "/home/hatch/workspace/custom-connectors/custom.youtube/bin")
from yt_api import search, videos
base = pathlib.Path.home()/"workspace/goals/ctrl-ahead-os-ai-video/files/pipeline/data/portfolio/2026-W43/stage_narrowing"
after=(dt.datetime.now(dt.timezone.utc)-dt.timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
now=dt.datetime.now(dt.timezone.utc)
def secs(d):
    m=re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', d or '')
    return int(m.group(1) or 0)*3600+int(m.group(2) or 0)*60+int(m.group(3) or 0) if m else 9999
chosen=[("Model comparisons","GPT vs Claude"),("Open-source model spotlights","open source AI model"),("AI video generation","AI video generation"),("AI coding agents","Claude Code tutorial"),("AI for small business","AI for small business")]
out={}
searches=0
for lane,q in chosen:
    for kind,qq in [("general",q),("shorts_search",q+" shorts")]:
        s=search(qq, after, 25); searches+=1
        ids=[i["id"]["videoId"] for i in s.get("items",[])]
        vids=[]
        if ids:
            for it in videos(ids).get("items",[]):
                pub=dt.datetime.fromisoformat(it["snippet"]["publishedAt"].replace("Z","+00:00")); age=max(1,(now-pub).total_seconds()/3600); views=int(it["statistics"].get("viewCount",0))
                vids.append({"id":it["id"],"title":it["snippet"]["title"],"channel":it["snippet"]["channelTitle"],"publishedAt":it["snippet"]["publishedAt"],"views":views,"velocity":round(views/age,2),"duration":it["contentDetails"].get("duration"),"duration_s":secs(it["contentDetails"].get("duration")),"url":f"https://youtube.com/watch?v={it['id']}"})
        vids.sort(key=lambda x:-x["velocity"])
        out.setdefault(lane,{})[kind]=vids
        print(lane, kind, len(vids), flush=True)
    allv=out[lane]["general"]+out[lane]["shorts_search"]
    # dedupe by id, keep highest velocity
    uniq={}
    for v in allv: uniq.setdefault(v["id"],v)
    allv=list(uniq.values())
    shorts=sorted([v for v in allv if v["duration_s"]<=60], key=lambda x:-x["velocity"])[:5]
    longs=sorted([v for v in allv if v["duration_s"]>=180], key=lambda x:-x["velocity"])[:5]
    out[lane]["refs_shorts_5"]=shorts; out[lane]["refs_longs_5"]=longs
    print(f"  -> shorts {len(shorts)} longs {len(longs)}", flush=True)
json.dump({"snapshot_utc":now.isoformat(),"searches_used_stage2":searches,"lanes":out}, open(base/"stage2_references_2026-10-26.json","w"), indent=1)
print("searches stage2:", searches)
