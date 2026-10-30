#!/usr/bin/env python3
"""GitHub trending via the official Search API — no HTML scraping.
Usage: GITHUB_TOKEN=... python3 github_trending.py --days 7 --out data/raw/<week>/github.json
Star velocity: for repos created in the window, stars/age_days is labelled as such.
For older repos, 7-day velocity needs a previous snapshot — this script records
stars_now and, if a previous file is given, stars_7d = stars_now - stars_then.
No token? Unauthenticated limit is 60/hr — the script stops, it does not retry in a loop.
"""
import argparse, json, os, sys, urllib.request, urllib.parse, datetime
API="https://api.github.com/search/repositories"
def req(url, token):
    r=urllib.request.Request(url, headers={"Accept":"application/vnd.github+json","User-Agent":"ctrl-ahead-os"})
    if token: r.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(r, timeout=30) as resp: return json.load(resp)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--topics", default="ai-tools,llm,ai-agent,local-llm")
    ap.add_argument("--out", required=True); ap.add_argument("--prev", default="")
    a=ap.parse_args()
    since=(datetime.date.today()-datetime.timedelta(days=a.days)).isoformat()
    prev={}
    if a.prev and os.path.exists(a.prev):
        for repo in json.load(open(a.prev)).get("repos", []): prev[repo["full_name"]]=repo.get("stars",0)
    repos=[]
    for topic in a.topics.split(","):
        q=f"topic:{topic.strip()} created:>={since}"
        data=req(f"{API}?q={urllib.parse.quote(q)}&sort=stars&order=desc&per_page=30", os.environ.get("GITHUB_TOKEN",""))
        for it in data.get("items", []):
            created=datetime.date.fromisoformat(it["created_at"][:10]); age=max(1,(datetime.date.today()-created).days)
            repos.append({"full_name":it["full_name"],"url":it["html_url"],"description":it.get("description"),
                "stars":it["stargazers_count"],"forks":it["forks_count"],"language":it.get("language"),
                "pushed_at":it.get("pushed_at"),"topic":topic,
                "stars_7d": (it["stargazers_count"]-prev[it["full_name"]]) if it["full_name"] in prev else None,
                "stars_per_day": round(it["stargazers_count"]/age,2) if age<=a.days*2 else None,
                "star_velocity_label": "stars_now_minus_prev_snapshot" if it["full_name"] in prev else "stars_per_day_new_repo_only"})
    # dedup, rank by stars_7d if present else stars
    seen={}
    for r in repos: seen[r["full_name"]]=r
    ranked=sorted(seen.values(), key=lambda x: (x["stars_7d"] if x["stars_7d"] is not None else x["stars"]), reverse=True)
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    json.dump({"generated_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"days":a.days,"repos":ranked[:100]}, open(a.out,"w"), indent=2)
    print(f"wrote {a.out}: {len(ranked)} repos, top: {ranked[0]['full_name'] if ranked else 'none'}")
if __name__=="__main__": main()
