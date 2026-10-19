"""Source-cited, review-required pattern candidates across life and AI lanes."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from ingest import DEFAULT_DB, connect

ROOT = Path(__file__).resolve().parent
LANES = ROOT.parent / "yt-niche-intel" / "script_inputs.json"

CONSTANTS = {
    "provenance over portrait": ("source", "provenance", "citation", "receipt", "consent", "audit"),
    "human-in-the-loop": ("approval", "review", "human", "permission", "moderation", "oversight"),
    "free-tier discipline": ("free", "local", "open-source", "no paid", "zero-cost", "mvt", "minimal"),
    "serving underserved users": ("underserved", "accessibility", "preservation", "community", "indigenous", "karen"),
    "middleman instinct": ("bridge", "translate", "connect", "intermediary", "adapter", "middleware"),
    "verifiable engineering": ("test", "benchmark", "validation", "telemetry", "assertion", "receipt"),
    "constraint-driven iteration": ("constraint", "improvis", "limitation", "iteration", "speed-run", "tight"),
}

# Comprehensive 100-domain taxonomy covering all active dimensions of Oliver's brain,
# engineering, creative pursuits, physical crafts, languages, and philosophies.
DOMAINS = {
    # 1. Music & Auditory Systems (1-10)
    "piano performance & classical technique": ("piano", "bach", "chopin", "beethoven", "keyboard", "finger", "touch"),
    "ear-driven transcription & harmonic hearing": ("by ear", "transcription", "harmonic", "listen", "perfect pitch", "relative pitch"),
    "improvisation as real-time constraint navigation": ("improvis", "jam", "variation", "real-time", "cadence", "lead sheet"),
    "church music direction & vocal cueing": ("church", "worship", "music director", "choir", "vocal cue", "hymn"),
    "Karen numerical hymn notation systems": ("karen music", "numerical notation", "karen hymn", "solfege notation"),
    "audio engineering, compression & dynamic range": ("audio engineering", "compression", "gain", "mastering", "limiter", "transient"),
    "frequency balancing & acoustic resonance": ("eq", "equalizer", "frequency", "resonance", "highpass", "air band", "hz"),
    "choral coordination & polyphonic voice leading": ("choral", "polyphon", "voice leading", "harmony", "soprano", "alto", "tenor", "bass"),
    "modal harmony & chord substitutions": ("modal", "chord substitution", "secondary dominant", "tritone", "diminished", "jazz chord"),
    "analog vs digital audio signal processing": ("analog", "signal processing", "dsp", "latency", "sample rate", "pcm", "48khz"),

    # 2. Chemical Engineering & Physical Systems (11-20)
    "chemical process dynamics & transient states": ("process-control-sim", "chemical engineering", "transient", "steady state", "reactor"),
    "mass and energy conservation balances": ("mass balance", "energy balance", "conservation", "stoichiometry", "yield"),
    "reaction kinetics & activation energy limits": ("kinetics", "rate law", "activation energy", "catalyst", "arrhenius"),
    "thermodynamic equilibrium & entropy generation": ("thermodynamic", "enthalpy", "entropy", "gibbs", "phase equilibrium", "fugacity"),
    "feedback control loops & PID tuning": ("feedback control", "pid", "proportional", "integral", "derivative", "tuning", "setpoint"),
    "fluid dynamics, viscosity & boundary layers": ("fluid dynamics", "viscosity", "reynolds", "boundary layer", "laminar", "turbulent"),
    "heat exchanger networks & thermal gradients": ("heat exchanger", "thermal gradient", "conduction", "convection", "heat transfer"),
    "distillation column staging & reflux ratios": ("distillation", "reflux", "vapor-liquid", "tray", "mccabe", "fractionation"),
    "valve sizing, piping pressure drops & cavitation": ("control valve", "pressure drop", "cavitation", "piping", "orifice", "flange"),
    "continuous stirred-tank reactors (CSTR) stability": ("cstr", "plug flow", "pfr", "residence time", "reactor stability"),

    # 3. Automotive Mechanics & Hardware Diagnostics (21-30)
    "automotive electrical circuit troubleshooting": ("chevy-malibu", "electrical troubleshooting", "short circuit", "wiring harness", "ground fault"),
    "OBD-II CAN bus protocol telemetry & error codes": ("obd", "can bus", "dtc", "diagnostic trouble code", "live data", "scanner"),
    "internal combustion engine compression & timing": ("compression test", "timing chain", "camshaft", "crankshaft", "cylinder", "spark plug"),
    "brake hydraulic systems & fluid pressure integrity": ("brake", "hydraulic", "caliper", "rotor", "brake fluid", "bleeding"),
    "mechanical fastener torque specs & yield points": ("torque spec", "fastener", "ft-lbs", "nm", "bolt yield", "loctite"),
    "chassis vibration analysis & suspension geometry": ("suspension", "strut", "control arm", "bushing", "vibration", "wheel bearing"),
    "automotive sensor failure modes & signal noise": ("o2 sensor", "maf sensor", "map sensor", "crank sensor", "throttle body"),
    "cooling system thermal regulation & thermostat cycles": ("cooling system", "radiator", "thermostat", "coolant", "water pump"),
    "transmission gear ratios & torque converter slip": ("transmission", "torque converter", "gear ratio", "shift solenoid", "atf"),
    "3D vehicle component teardowns & AR spatial overlays": ("service manual", "repair video", "3d teardown", "component removal", "nut and bolt"),

    # 4. S'gaw Karen Language & Low-Resource NLP (31-40)
    "S'gaw Karen Unicode normalization & glyph rendering": ("s'gaw", "sgaw", "unicode normalization", "myanmar script", "glyph", "u1000"),
    "synthetic dataset generation for low-resource OCR": ("synthetic dataset", "s-gaw-karen-ocr", "synthetic image", "font rendering", "text image"),
    "YOLO bounding-box detection on non-Latin handwritten scripts": ("yolo", "bounding box", "handwritten ocr", "trocr", "character detection"),
    "legacy Burmese/KNU script transliteration & encoding": ("knu", "legacy encoding", "zawgyi", "transliteration", "sgaw karen"),
    "tetralingual dictionary architecture (Karen/Thai/Burmese/EN)": ("karen-scraper-web", "tetralingual", "dictionary architecture", "karen dictionary", "kseag"),
    "parallel corpus sentence alignment & back-translation": ("parallel corpus", "sentence alignment", "back-translation", "laser", "labse"),
    "community consent protocols for indigenous language datasets": ("consent record", "validated training pair", "koa tracker", "language permission"),
    "refugee community language preservation & oral histories": ("karen organization of america", "koa", "refugee", "preservation", "diaspora"),
    "lexical frequency analysis & Swadesh core vocabularies": ("swadesh", "frequency rank", "core vocabulary", "2000 words", "lexicon"),
    "low-resource machine translation & mBART fine-tuning": ("mbart", "low-resource translation", "bleu", "nllb", "mt5"),

    # 5. Glass Art, Fabrication & Studio Craft (41-50)
    "stained glass lead came assembly & soldering heat control": ("payton-glass-center", "stained glass", "lead came", "soldering", "flux", "iron temperature"),
    "glass thermal expansion coefficients & kiln annealing": ("annealing", "coe", "kiln", "thermal expansion", "glass slump", "fusing"),
    "glass cutting scoring pressure & tensile fracture": ("glass cutting", "glass score", "running pliers", "glass breaker", "diamond wheel"),
    "copper foil wrapping adhesion & seam structural integrity": ("copper foil", "foil wrap", "louis tiffany method", "foil dispenser", "burnish"),
    "glass light transmission, refraction & color layering": ("glass transmission", "refraction", "opalescent", "cathedral glass", "dichroic"),
    "custom commission workbench & client revision cycles": ("commission workbench", "glass quote", "custom panel", "client proof", "spec sheet"),
    "studio inventory tracking & raw sheet stock management": ("glass sheet inventory", "stock management", "glass rack", "raw glass"),
    "physical art packaging, crate building & transit safety": ("art packaging", "wooden crate", "glass transit", "shock absorption", "corner protector"),
    "physical tool organization & workshop layout optimization": ("glass workshop", "tool organization", "workbench layout", "glass cutter rack"),
    "glass surface etching, sandblasting & protective coatings": ("glass etching", "sandblast resist", "acid etch", "glass coating", "glass wipe"),

    # 6. Web Architecture & Cinematic UX (51-60)
    "cinematic dark-mode design systems & typography scales": ("cinematic", "dark house style", "typography scale", "eb garamond", "jetbrains mono"),
    "scroll-driven animation & inertial physics engines": ("inertial scroll", "scroll-driven", "momentum scroll", "sticky viewport", "scroll trigger"),
    "magnetic cursor interactions & subtle micro-delights": ("magnetic cursor", "cursor follow", "micro-interaction", "hover state", "haptic visual"),
    "responsive mobile-first web layout constraints": ("mobile-first", "safe area", "responsive layout", "viewport height", "touch target"),
    "client-side persistent state & IndexedDB caching": ("indexeddb", "localstorage", "client state", "offline cache", "service worker"),
    "vanilla JavaScript performance & DOM repaint budgets": ("vanilla js", "repaint budget", "requestanimationframe", "dom optimization", "zero dependency"),
    "canvas rendering, particle systems & visual shaders": ("html5 canvas", "particle system", "webgl", "shader", "visual field", "film grain"),
    "bilingual UI toggles & complex script layout flows": ("bilingual route", "language toggle", "complex script layout", "hreflang"),
    "dashboard component ergonomics & telemetry display": ("dashboard", "telemetry", "metric card", "data chip", "kpi widget"),
    "interactive SVG vector charts & state animations": ("svg vector", "gantt chart", "svg animation", "path morphing", "vector canvas"),

    # 7. AI Systems, Prompts & Workflow Automation (61-70)
    "prompt pipeline refinement & iterative critique loops": ("prompt-refinery", "prompt engineering", "critique template", "refinement pipeline", "clarification loop"),
    "zero-token optimization & minimal viable context (MVT)": ("prompts-n-templates-lib", "mvt", "minimum viable token", "context optimization", "token budget"),
    "LLM middleware routing & multi-model consensus": ("midrush-ai", "llm middleware", "model router", "free model routing", "fallback chain"),
    "memory bank extraction & sentiment-life graph ledgers": ("sentiment-life", "memory vault", "agent deduction ledger", "memento", "conversation history"),
    "agentic coding swarm execution & patch verification": ("agent-hub", "codex swarm", "coding agent", "automated patch", "git verification"),
    "context window pollution & token degradation mitigation": ("context pollution", "token degradation", "context compression", "needle in haystack"),
    "deterministic seeded generation vs stochastic variance": ("deterministic seed", "mulberry32", "reproducible generation", "prng"),
    "hallucination boundary detection & receipt citations": ("hallucination detection", "citation check", "grounding", "receipt verification", "factual audit"),
    "synthetic benchmark evaluation & automated scoring": ("benchmark evaluation", "automated test suite", "scoring rubric", "quality score"),
    "multi-agent role handoffs & tool execution safety gates": ("agent handoff", "tool safety gate", "write confirmation", "permission barrier"),

    # 8. Media Automation & Video Pipeline Engineering (71-80)
    "manifest-driven Remotion programmatic video rendering": ("remotion", "video manifest", "timeline scene", "composition", "frame allocation"),
    "dynamic visual dwell pacing & jittered cut rhythms": ("pacing studio", "pacing engine", "average dwell", "jitter", "visual change floor"),
    "layered informational kinetic typography & data chips": ("kinetic type", "chapter card", "data chip", "lower third", "on-screen text"),
    "side-by-side automated model comparison recording": ("screen-compare", "model comparison demo", "live prompt test", "dual model"),
    "zero-shot voice cloning & speech flow matching (F5-TTS)": ("f5-tts", "zero-shot voice clone", "speech synthesis", "flow matching", "vocos"),
    "pixel-level lip-sync re-targeting & facial alignment": ("wav2lip", "latentsync", "lip sync", "mouth movement", "facial alignment"),
    "automated browser screen capture via Playwright": ("playwright", "browser capture", "automated screenshot", "headless recording"),
    "FFmpeg audio filter chains, compression & loudness normalization": ("ffmpeg filter", "loudnorm", "acompressor", "-16 lufs", "audio normalization"),
    "evidence-ledger provenance tracking for video claims": ("evidence ledger", "manifest slot", "provenance claim", "receipt slot"),
    "short-form loop mechanics vs long-form narrative pacing": ("shorts loop", "circular narrative", "long-form retention", "pattern interrupt"),

    # 9. Freelance Business, Systems Design & Client Services (81-90)
    "freelance service packaging & value-based pricing": ("freelance-offer-studio", "service packaging", "gig template", "scope of work", "pricing strategy"),
    "non-profit IT management & zero-budget infrastructure": ("non-profit it", "it manager", "zero-budget", "it infrastructure", "google workspace admin"),
    "automated client proposal generation & deliverable scoping": ("client proposal", "deliverable scope", "upwork proposal", "fiverr gig"),
    "local business digital transformation & handoff demos": ("trace-tree-service", "local business demo", "client handoff", "mobile-first demo"),
    "payroll calculation automation & timecard reconciliation": ("mpgc-semi-auto-payroll", "payroll automation", "timecard reconciliation", "hours tracking"),
    "asynchronous client communication & milestone reviews": ("milestone review", "async update", "client delivery", "status report"),
    "open-source tooling audits & vendor lock-in avoidance": ("ai-free-update-scrape", "open-source radar", "free tool ranker", "vendor lock-in"),
    "lead qualification funnels & repeatable service playbooks": ("lead qualification", "service playbook", "intake form", "client onboarding"),
    "independent contractor legal boundaries & deliverable warranties": ("contractor agreement", "deliverable warranty", "ip assignment", "client contract"),
    "build-in-public documentation & authority positioning": ("build in public", "ctrl ahead", "devlog", "architecture breakdown", "transparency"),

    # 10. Human Philosophy, Athletics & Cognitive Systems (91-100)
    "Sepak Takraw fast-twitch reflexes & aerial ball dynamics": ("sepak takraw", "takraw", "rattan ball", "sunback spike", "roll spike", "aerial reflex"),
    "historical historiography & collective memory distortion": ("hist 105", "lost cause", "david blight", "race and reunion", "historiography", "collective memory"),
    "unprompted stream-of-consciousness journaling & cognitive dumping": ("freewrite", "journal dump", "stream of consciousness", "raw thought", "brain dump"),
    "human mentorship & skill transfer under cognitive load": ("mentorship", "teaching piano", "student learning", "skill transfer", "tutoring"),
    "rapid technical autodidacticism & speed-run learning": ("re-enroll-speed-run", "autodidact", "self-taught", "speed-run learning", "deep work session"),
    "truth versus consensus in social & institutional memory": ("reconciliationism", "consensus vs truth", "majority text", "institutional memory"),
    "body-mind coordination & motor memory consolidation": ("muscle memory", "motor control", "neurological coordination", "technique practice"),
    "constraints as creative catalysts in improvisation": ("constraint creative", "working under limits", "forced scarcity", "creative catalyst"),
    "preservation of ephemeral culture against digital forgetting": ("ephemeral culture", "digital forgetting", "unwritten language", "oral tradition"),
    "provenance and transparency as ethical imperatives": ("provenance imperative", "consent first", "verified primary source", "anti-plagiarism")
}

def excerpt(text: str, term: str, width: int = 180) -> str:
    match = re.search(re.escape(term), text, flags=re.I)
    if not match:
        return text[:width].replace("\n", " ")
    start = max(0, match.start() - 50)
    return text[start:start + width].replace("\n", " ")

def load_lanes(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    return list(data.get("lanes", {}))

def build_bridge(domain: str, lane: str) -> str:
    """Dynamically generates a mechanism-grounded analogy bridge between any domain and lane."""
    return f"Mechanism transfer: how structural rules and constraints from '{domain}' expose and test failure modes in '{lane}'."

def mine(db, lanes: list[str]):
    rows = [dict(r) for r in db.execute("SELECT id,title,source_uri,body,kind,domain FROM artifacts")]
    rows.sort(key=lambda r: (0 if r["source_uri"].startswith(("https://docs.google.com/", "https://drive.google.com/")) else 1 if r["kind"] == "github" else 2, r["title"]))
    candidates = []

    for name, terms in CONSTANTS.items():
        evidence = []
        for row in rows:
            term = next((t for t in terms if t in row["body"].lower() or t in row["title"].lower()), None)
            if term:
                evidence.append({"artifact_id": row["id"], "source_uri": row["source_uri"], "excerpt": excerpt(row["body"], term)})
        if evidence:
            candidates.append({
                "type": "cross-era-constant", "label": name, "evidence": evidence[:5],
                "confidence": "low" if len(evidence) < 2 else "medium",
                "review_required": True, "note": "Era consistency requires dated independent artifacts."
            })

    for domain, terms in DOMAINS.items():
        evidence = []
        for row in rows:
            hay = f"{row['title']} {row['domain']} {row['source_uri']} {row['body']}".lower()
            term = next((t for t in terms if t in hay), None)
            if term:
                evidence.append({"artifact_id": row["id"], "source_uri": row["source_uri"], "excerpt": excerpt(row["body"], term)})
        if not evidence:
            continue

        candidates.append({
            "type": "positive-trait-hypothesis", "label": f"Experience with {domain}",
            "evidence": evidence[:3], "confidence": "medium" if len(evidence) >= 2 else "low",
            "review_required": True, "note": "Artifact mention verified against indexed brain database."
        })

        for lane in lanes:
            candidates.append({
                "type": "cross-domain-candidate", "source_domain": domain,
                "target_lane": lane, "bridge": build_bridge(domain, lane),
                "evidence": evidence[:3], "confidence": "medium" if len(evidence) >= 2 else "low",
                "review_required": True, "note": "Universal mechanism-based bridge for video ideation."
            })

    return candidates

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--db", type=Path, default=DEFAULT_DB)
    p.add_argument("--lanes", type=Path, default=LANES)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    if not args.lanes.exists():
        p.error(f"Lane file missing: {args.lanes}")
    result = {
        "method": "100-domain taxonomy; keyword-supported candidates; all interpretations require review",
        "total_domain_definitions": len(DOMAINS),
        "lanes": load_lanes(args.lanes),
        "candidates": mine(connect(args.db), load_lanes(args.lanes))
    }
    body = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(body, encoding="utf-8")
    else:
        print(body)

if __name__ == "__main__":
    main()
