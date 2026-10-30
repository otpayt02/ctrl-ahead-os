"""Read-only project setup scanner. Usage: python3 project_setup_scan.py <dir>"""
import os, sys, json
root=sys.argv[1] if len(sys.argv)>1 else "."
found={}
for dirpath, dirs, files in os.walk(root):
    dirs[:]=[d for d in dirs if d not in (".git",".venv","node_modules","__pycache__")]
    for f in files:
        p=os.path.join(dirpath,f); rel=os.path.relpath(p,root)
        ext=os.path.splitext(f)[1].lower()
        found.setdefault(ext,[]).append(rel)
        if f in ("package.json","requirements.txt","pyproject.toml","Dockerfile",".github/workflows/ingest.yml","GOAL.md","SKILL.md"):
            found.setdefault("KEY_FILES",[]).append(rel)
recs=[]
if ".py" in found: recs.append({"need":"Python skill / ffmpeg / PIL","reason":f"{len(found['.py'])} Python files found"})
if ".md" in found: recs.append({"need":"Documents skill","reason":f"{len(found['.md'])} Markdown files found"})
if any("workflow" in x for x in found.get("KEY_FILES",[])): recs.append({"need":"GitHub Actions workflow review","reason":"workflow file found"})
if ".json" in found: recs.append({"need":"JSON / manifest handling","reason":f"{len(found['.json'])} JSON files found"})
print(json.dumps({"project":root,"file_types":{k:len(v) for k,v in found.items()},"key_files":found.get("KEY_FILES",[]),"recommendations":recs},indent=2))
