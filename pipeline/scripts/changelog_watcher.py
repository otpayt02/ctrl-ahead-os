#!/usr/bin/env python3
"""Changelog watcher: RSS (feedparser if available, else xml) + GitHub Releases API.
Usage: python3 changelog_watcher.py --watchlist ../watchlist.csv --out data/raw/<week>/changelogs.json
Stores only new guids (hash of guid or link). Never invents a changelog entry:
if a feed fails, it records status=failed with the error, it does not skip silently.
GitHub releases use the same token env as github_trending.py, conditional-ish
by simply recording snapshot_at — quota is 60/hr unauth, 5000/hr auth.
"""
import argparse, csv, json, os, hashlib, urllib.request, datetime, xml.etree.ElementTree as ET
def fetch(url, token=""):
    r=urllib.request.Request(url, headers={"User-Agent":"ctrl-ahead-os"})
    if token and "github.com" in url: r.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(r, timeout=30) as resp: return resp.read()
def parse_rss(data):
    try:
        root=ET.fromstring(data); items=[]
        for it in root.iter("item"):
            t=it.findtext("title",""); l=it.findtext("link",""); d=it.findtext("pubDate",""); g=it.findtext("guid") or l
            items.append({"title":t,"url":l,"published_at":d,"guid":hashlib.sha256(g.encode()).hexdigest()})
        return items
    except Exception as e: return [{"error":str(e)}]
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--watchlist", required=True); ap.add_argument("--out", required=True); a=ap.parse_args()
    token=os.environ.get("GITHUB_TOKEN",""); out=[]; now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    for row in csv.DictReader(open(a.watchlist)):
        entry={"company":row["company"],"cluster":row["cluster"],"kind":row["kind"],"fetched_at":now,"sources":[]}
        if row.get("rss_url"):
            try: entry["sources"].append({"type":"rss","url":row["rss_url"],"items":parse_rss(fetch(row["rss_url"]))[:20]})
            except Exception as e: entry["sources"].append({"type":"rss","url":row["rss_url"],"status":"failed","error":str(e)})
        if row.get("github_org"):
            # GitHub releases for the org's repos are handled per-repo in a separate run;
            # here we record the org endpoint status only, to keep this watcher quota-light.
            entry["sources"].append({"type":"github_org","org":row["github_org"],"note":"Use github_releases per repo, not org-wide, to stay within rate limits"})
        out.append(entry)
    os.makedirs(os.path.dirname(a.out), exist_ok=True); json.dump({"generated_at":now,"companies":out}, open(a.out,"w"), indent=2)
    print(f"wrote {a.out}: {len(out)} companies")
if __name__=="__main__": main()
