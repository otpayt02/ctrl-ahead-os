# 006 — The 5-Day Roadmap, Explained
## Script: Oliver's verbatim text, supplied 2026-10-30 — "script stays the same as this"
## This is the narration source for the premium redo (v3). Do not edit the words.

[0:00 – HOOK]
(Fast montage: terminal deploying, app loading, dashboards)

"There's a roadmap going around claiming you can build a production-ready full-stack web app in five days, almost free. It's real — and in the next nine and a half minutes I'm going to explain every tool in it: what it is, why you need it, what breaks if you skip it, and how to actually do it. If you can follow a recipe, you can follow this."

[0:25 – INTRO]

"Five days, about 38 hours, React frontend, Python backend, pay-per-request everything. Day one sets up your tools, day two builds what users see, day three the logic, day four the memory, day five you go live. Let's go."

[0:45 – DAY 1: SETUP (7 hrs)]

GIT

"Git, created in 2005 when Linus Torvalds built a version-control system in about ten days. What it is: a time machine for your code — every working version saved as a checkpoint. Why you need it: production code changes daily, and you need undo. Skip it, and one bad edit costs you a day of guessing what changed. How: git init, commit every time something works, push to GitHub."

AWS ACCOUNT

"Your AWS account. Amazon's cloud launched in 2006 with one storage service. What it is: where everything else in this video lives, metered like a utility. Why: an app with no traffic costs almost nothing. Skip it and you're building a website that only you can see. How: sign up, stay in the free tier, done in fifteen minutes."

DOCKER

"Docker, open-sourced in 2013 by a tiny startup called dotCloud . What it is: a box that packs your app plus everything it needs to run. Why: the box behaves identically on your laptop and on the live site. Skip it and you'll meet the 'works on my machine' bug on launch day. How: one Dockerfile, docker build — that's the 30-minute version."

CURSOR + CLAUDE

"Cursor, released in 2023 by four MIT students, an editor with AI built in — paired with Claude Sonnet 4, it's a junior developer who types instantly. Why: the five-day timeline only exists because the AI writes the boilerplate while you review. Skip it and this is a five-week project. How: install it, open your project, and describe what you want in plain English."

AWS AMPLIFY

"Amplify, born in 2017 . What it is: a publisher — every time you push code, it automatically republishes your live site, with security certificates included. Why: launch-day plumbing handled for free. Skip it and you're manually uploading files and babysitting expired certificates. How: connect your GitHub repo once, and never think about it again."

AWS SAM

"And SAM, from 2018 . What it is: a blueprint — your entire backend described in one text file, built by a single command. Why: reproducible, undoable infrastructure instead of clicking through twenty consoles. Skip it and your setup exists in no one's head, exactly once. How: write a template.yaml, deploy with the SAM CLI. Three hours today, saves your whole week."

[3:45 – DAY 2: UI (8 hrs)]

REACT

"Day two. React, built at Facebook by Jordan Walke, released in 2013 . What it is: Lego for interfaces — build a button or calendar once, snap it in anywhere. Why: it's the industry standard, so tutorials and help are everywhere. Skip it and you're hand-crafting every page from scratch. How: scaffold the project, build each page as bricks, done in half an hour of setup."

VIBE CODING

"Then seven hours building the whole interface by prompting the AI — with one rule: fake data, no backend. Why: you make the site look and feel finished before the plumbing exists. Skip this discipline and you'll spend the day debugging connections instead of building. How: prompt one component at a time, click through it, refine."

API GATEWAY

"Last half hour: API Gateway, launched 2015. What it is: the front door — it checks every incoming request before anything touches your code. Why: security, throttling, and routing in one place. Skip it and browsers are poking your backend directly, unlocked. How: create a REST API, one route per action, and Day 3 has something to plug into."

[5:15 – DAY 3: BACKEND (8 hrs)]

LAMBDA

"Day three, the logic — and the star: AWS Lambda, announced in 2014 . What it is: a motion-sensor light. Your code turns on when a request arrives, off when it's done — you pay per flip, not for an always-on bulb. Why: no traffic means near-zero cost, and 5,000 users scale automatically. Skip it and you're renting a server that runs 24/7 for a site nobody's found yet. How: write a Python handler and connect it to the Gateway route."

AI BACKEND BUILD

"Six hours of AI-assisted development: validation, pricing rules, emails — prompted into existence one endpoint at a time, with TODO comments where caching belongs later. How: small scope. By tonight, creating, reading, and canceling works."

OPTIONALS

"Two upgrades for later: FastAPI, from 2019 , when one request involves many slow steps at once. And SQS — the ticket dispenser: it was AWS's first service — it queues a flood of requests so none bounce. Skip both for now; add them when traffic demands it."

[6:45 – DAY 4: DATA (8 hrs)]

DYNAMODB

"Day four, your app gets a memory: DynamoDB, released in 2012, grown from the database Amazon built for its own shopping cart . What it is: a filing cabinet with lookup codes — instant answers, no rigid schema. Why: pay per request, millisecond speed, change your data shape weekly. Skip it and you're either paying for an idle database server or freezing your app's structure early. How: partition by what you'll ask for, sort by the piece ID — design the lookups first, always."

TESTING

"Five hours wiring real reads and writes end to end, two hours testing both halves separately with logging on. Why: bugs found on day four cost minutes; found on day five, they cost your launch. Skip it and your users are your QA team."

OPTIONALS

"Later, not now: RDS, from 2009 — the strict spreadsheet database, for the day payments get serious. And S3, Amazon's very first service — an infinite garage for files and video. How you'll know: you'll need reports, or you'll need file storage. Until then, skip."

[8:15 – DAY 5: LAUNCH (7 hrs)]

DEPLOY

"Day five. Frontend: git push — Amplify republishes automatically, live HTTPS site. Backend: one SAM command ships every function, route, and database permission together, versioned and undoable. This is the payoff of Days 1 and 4. How: connect GitHub to Amplify, run the deploy, watch it all go green."

CLOUDWATCH

"Then CloudWatch, from 2009. What it is: a heart monitor plus security cameras for your app — every request leaves a log, alarms email you when errors spike. Why: when it breaks at 2 AM, this is how you know before your users tell you. Skip it and failures happen silently while angry customers wait. How: turn on logging, set one alarm on errors. That's 90% of the value."

OPTIONALS

"And the polish, when you're ready: Grafana — a 2014 side project that became the standard dashboard for gauges and graphs — and X-Ray, package-tracking for every request, showing which step is slow. Nice on day one, essential by day one thousand."

[9:05 – CLOSE]

"That's the whole roadmap: setup, frontend, backend, memory, launch. Thirty-eight hours, near-zero cost until you have users, and every tool here does one job you can name. Follow the five days in order — skip nothing on Day 1 — and ship something real this week. Subscribe if this mapped it out for you, and comment which day you're starting with."
