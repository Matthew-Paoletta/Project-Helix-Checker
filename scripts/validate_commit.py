#!/usr/bin/env python3
import argparse, json, os, re, urllib.request
from urllib.error import HTTPError

def gh_get(url, token=None):
    req = urllib.request.Request(url, headers={"Accept":"application/vnd.github+json","User-Agent":"project-helix-checker"})
    if token: req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req) as r: return json.loads(r.read().decode())

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--repo", required=True); p.add_argument("--commit", required=True)
    p.add_argument("--rules", default="config/validation-rules.json")
    a = p.parse_args()
    rules = json.load(open(a.rules))
    try:
        c = gh_get(f"https://api.github.com/repos/{a.repo}/commits/{a.commit}", os.getenv("GITHUB_TOKEN"))
    except HTTPError as e:
        print(json.dumps({"status":"ERROR","error":f"HTTP {e.code}: {e.reason}"}, indent=2)); raise SystemExit(2)

    msg = c.get("commit",{}).get("message","")
    files = c.get("files",[])
    changed = [f.get("filename","") for f in files]
    adds = sum(f.get("additions",0) for f in files); dels = sum(f.get("deletions",0) for f in files)

    checks = []
    ok = all(re.search(rx, msg or "") for rx in rules["commit_message"]["required_regex"])
    checks.append({"name":"commit_message.required_regex","passed":ok})
    ok2 = not any(re.search(rx, msg or "") for rx in rules["commit_message"]["forbidden_regex"])
    checks.append({"name":"commit_message.forbidden_regex","passed":ok2})
    bad = any(any(re.search(rx, p) for p in changed) for rx in rules["changed_files"]["forbidden_path_regex"])
    checks.append({"name":"changed_files.forbidden_path_regex","passed":not bad})
    checks.append({"name":"changed_files.max_files_changed","passed":len(changed) <= rules["changed_files"]["max_files_changed"]})
    checks.append({"name":"diff_limits.max_additions","passed":adds <= rules["diff_limits"]["max_additions"]})
    checks.append({"name":"diff_limits.max_deletions","passed":dels <= rules["diff_limits"]["max_deletions"]})

    failed = sum(1 for c in checks if not c["passed"])
    out = {"status":"VALID" if failed==0 else "INVALID","commit":a.commit,"repository":a.repo,"checks":checks}
    print(json.dumps(out, indent=2))
    raise SystemExit(0 if failed==0 else 1)

if __name__ == "__main__":
    main()
