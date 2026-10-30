"""Read-only security scan. Reports file+pattern only, NEVER values. Usage: python3 security_scan.py <dir>"""
import os, sys, re
root=sys.argv[1] if len(sys.argv)>1 else "."
pats={"api_key_like":r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"][^'\"]{8,}","private_key":r"-----BEGIN (?:RSA )?PRIVATE KEY-----","url_with_creds":r"https?://[^:/\s]+:[^@\s]+@","aws_key":r"AKIA[0-9A-Z]{16}"}
findings=[]
for dirpath, dirs, files in os.walk(root):
    dirs[:]=[d for d in dirs if d not in (".git",".venv","node_modules","__pycache__")]
    for f in files:
        p=os.path.join(dirpath,f)
        try: txt=open(p,errors="ignore").read()
        except Exception: continue
        for name,pat in pats.items():
            if re.search(pat,txt): findings.append({"file":os.path.relpath(p,root),"pattern":name,"verified":"pattern present in file; value NOT shown"})
print(f"findings: {len(findings)}")
for x in findings: print(x)
