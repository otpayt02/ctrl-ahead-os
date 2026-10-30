import csv, json, sys, datetime as dt, pathlib
sys.path.insert(0, "/home/hatch/workspace/custom-connectors/custom.youtube/bin")
from yt_api import search, videos
base = pathlib.Path.home()/"workspace/goals/ctrl-ahead-os-ai-video/files/pipeline/data/portfolio/2026-W43"
outdir = base/"stage_narrowing"; outdir.mkdir(exist_ok=True)
rows=list(csv.DictReader(open(pathlib.Path.home()/"workspace/goals/ctrl-ahead-os-ai-video/hidden_files/harvest/subniche_lanes.csv")))
lanes=[]; seen=set()
for r in rows:
    if r["subniche"] not in seen:
        seen.add(r["subniche"]); lanes.append(r)
print("lanes:", len(lanes))
after=(dt.datetime.now(dt.timezone.utc)-dt.timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
now=dt.datetime.now(dt.timezone.utc)
results=[]
searches=0
for lane in lanes:
    q=lane["seed_query"]
    try:
        s=search(q, after, 25); searches+=1
        ids=[i["id"]["videoId"] for i in s.get("items",[])]
        vids=[]
        if ids:
            v=videos(ids)
            for it in v.get("items",[]):
                pub=dt.datetime.fromisoformat(it["snippet"]["publishedAt"].replace("Z","+00:00"))
                age=max(1,(now-pub).total_seconds()/3600)
                views=int(it["statistics"].get("viewCount",0))
                vids.append({"id":it["id"],"title":it["snippet"]["title"],"channel":it["snippet"]["channelTitle"],"channelId":it["snippet"]["channelId"],"publishedAt":it["snippet"]["publishedAt"],"views":views,"velocity":round(views/age,2),"duration":it["contentDetails"].get("duration"),"is_short": "shorts" in it["snippet"].get("title","").lower()})
        vids.sort(key=lambda x:-x["velocity"])
        import statistics
        med=statistics.median([x["velocity"] for x in vids]) if vids else 0
        results.append({"lane":lane["subniche"],"cluster":lane["cluster"],"seed_query":q,"count":len(vids),"top":vids[:5],"median_velocity":round(med,2),"top_velocity":vids[0]["velocity"] if vids else 0})
        print(f"{lane['subniche']}: {len(vids)} videos, top vel {results[-1]['top_velocity']}, median {med:.1f}", flush=True)
    except Exception as e:
        print(f"{lane['subniche']}: ERROR {str(e)[:200]}", flush=True)
        results.append({"lane":lane["subniche"],"cluster":lane["cluster"],"seed_query":q,"error":str(e)[:300]})
json.dump({"snapshot_utc":now.isoformat(),"window":"7d","searches_used_stage1":searches,"lanes":results}, open(outdir/"stage1_general_2026-10-26.json","w"), indent=1)
print("searches:", searches)
