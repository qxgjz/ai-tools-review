#!/usr/bin/env python3
"""
AIToolCrux GitHub API Push with Pre-Deploy Audit Gate (v2.0)
- Runs pre_deploy_gate.py before pushing
- Blocks push if audit fails
- Uses GITHUB_TOKEN env var (no hardcoded secrets)
- Auto-detects changed files instead of hardcoded list

Usage:
  python push_via_api.py "commit message"          # Auto-detect changed files
  python push_via_api.py "commit message" file1.py file2.ts  # Specific files
  python push_via_api.py --skip-gate "message"     # Skip audit (emergency only)
"""

import requests
import json
import base64
import os
import sys
import subprocess
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Security: read token from env var, never hardcode
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
if not GITHUB_TOKEN:
    # Fallback: check .env file
    env_path = os.path.join(PROJECT_ROOT, ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("GITHUB_TOKEN="):
                    GITHUB_TOKEN = line.strip().split("=", 1)[1].strip().strip('"').strip("'")
                    break

REPO_OWNER = "qxgjz"
REPO_NAME = "ai-tools-review"
BRANCH = "main"

API_BASE = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "Content-Type": "application/json"
}


def run_pre_deploy_gate():
    """Run pre-deploy audit gate. Returns True if passed."""
    print("\n" + "=" * 60)
    print("RUNNING PRE-DEPLOY AUDIT GATE")
    print("=" * 60)

    gate_script = os.path.join(PROJECT_ROOT, "scripts", "pre_deploy_gate.py")
    if not os.path.exists(gate_script):
        print("  ⚠️  pre_deploy_gate.py not found, skipping gate")
        return True

    try:
        result = subprocess.run(
            [sys.executable, gate_script],
            cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=180
        )
        print(result.stdout[-2000:] if len(result.stdout) > 2000 else result.stdout)
        if result.stderr:
            print(result.stderr[-500:])

        if result.returncode != 0:
            print("\n  ❌ AUDIT GATE FAILED — push blocked")
            print("  Fix the issues above, then re-run.")
            return False
        print("\n  ✅ AUDIT GATE PASSED")
        return True
    except subprocess.TimeoutExpired:
        print("  ⚠️  Audit gate timed out (3min), blocking push as precaution")
        return False
    except Exception as e:
        print(f"  ⚠️  Audit gate error: {e}, blocking push as precaution")
        return False


def get_changed_files():
    """Get list of changed/untracked files via git."""
    files = set()

    # Modified/staged files
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=10
        )
        for f in result.stdout.strip().split("\n"):
            if f.strip():
                files.add(f.strip())
    except:
        pass

    # Untracked files
    try:
        result = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=10
        )
        for f in result.stdout.strip().split("\n"):
            if f.strip():
                files.add(f.strip())
    except:
        pass

    # Staged files
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=10
        )
        for f in result.stdout.strip().split("\n"):
            if f.strip():
                files.add(f.strip())
    except:
        pass

    return sorted(f for f in files if os.path.exists(os.path.join(PROJECT_ROOT, f)))


def get_latest_commit():
    response = requests.get(f"{API_BASE}/git/ref/heads/{BRANCH}", headers=HEADERS, timeout=30)
    response.raise_for_status()
    return response.json()["object"]["sha"]


def get_commit_tree(commit_sha):
    response = requests.get(f"{API_BASE}/git/commits/{commit_sha}", headers=HEADERS, timeout=30)
    response.raise_for_status()
    return response.json()["tree"]["sha"]


def create_blob(file_path):
    with open(file_path, "rb") as f:
        content = f.read()
    content_b64 = base64.b64encode(content).decode("utf-8")
    payload = {"content": content_b64, "encoding": "base64"}
    response = requests.post(f"{API_BASE}/git/blobs", headers=HEADERS, json=payload, timeout=60)
    response.raise_for_status()
    return response.json()["sha"]


def create_tree(base_tree_sha, file_blobs):
    tree_items = []
    for file_path, blob_sha in file_blobs.items():
        tree_items.append({
            "path": file_path, "mode": "100644", "type": "blob", "sha": blob_sha
        })
    payload = {"base_tree": base_tree_sha, "tree": tree_items}
    response = requests.post(f"{API_BASE}/git/trees", headers=HEADERS, json=payload, timeout=60)
    response.raise_for_status()
    return response.json()["sha"]


def create_commit(tree_sha, parent_sha, message):
    payload = {"message": message, "tree": tree_sha, "parents": [parent_sha]}
    response = requests.post(f"{API_BASE}/git/commits", headers=HEADERS, json=payload, timeout=60)
    response.raise_for_status()
    return response.json()["sha"]


def update_ref(commit_sha):
    payload = {"sha": commit_sha, "force": False}
    response = requests.patch(f"{API_BASE}/git/refs/heads/{BRANCH}", headers=HEADERS, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def main():
    if not GITHUB_TOKEN:
        print("❌ ERROR: GITHUB_TOKEN not set")
        print("   Set env var: $env:GITHUB_TOKEN='your_token'")
        print("   Or create .env file with GITHUB_TOKEN=your_token")
        sys.exit(1)

    # Parse args
    args = sys.argv[1:]
    skip_gate = "--skip-gate" in args
    if skip_gate:
        args.remove("--skip-gate")

    if not args:
        print("Usage: python push_via_api.py \"commit message\" [file1 file2 ...]")
        print("       python push_via_api.py --skip-gate \"message\"")
        sys.exit(1)

    commit_message = args[0]
    specific_files = args[1:] if len(args) > 1 else None

    print("=" * 60)
    print("AIToolCrux GitHub API Push (v2.0 with audit gate)")
    print("=" * 60)
    print(f"Commit: {commit_message[:60]}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Step 0: Pre-deploy audit gate
    if not skip_gate:
        if not run_pre_deploy_gate():
            print("\n❌ PUSH ABORTED — audit gate failed")
            sys.exit(1)
    else:
        print("\n⚠️  --skip-gate flag used, audit gate skipped (emergency only)")

    # Step 1: Determine files to push
    if specific_files:
        files_to_push = [f for f in specific_files if os.path.exists(os.path.join(PROJECT_ROOT, f))]
        print(f"\nFiles specified: {len(files_to_push)}")
    else:
        files_to_push = get_changed_files()
        print(f"\nChanged files detected: {len(files_to_push)}")
        for f in files_to_push[:15]:
            print(f"  + {f}")
        if len(files_to_push) > 15:
            print(f"  ... and {len(files_to_push) - 15} more")

    if not files_to_push:
        print("\n⚠️  No files to push")
        sys.exit(0)

    # Safety: don't push .env or secrets
    files_to_push = [f for f in files_to_push if not f.endswith(".env") and "secret" not in f.lower()]

    # Step 2: Get latest commit
    print("\n1. Getting latest commit...")
    latest_commit = get_latest_commit()
    print(f"   Latest: {latest_commit[:7]}")

    # Step 3: Get base tree
    print("2. Getting base tree...")
    base_tree = get_commit_tree(latest_commit)
    print(f"   Tree: {base_tree[:7]}")

    # Step 4: Create blobs
    print(f"3. Creating {len(files_to_push)} blobs...")
    file_blobs = {}
    for i, file_path in enumerate(files_to_push, 1):
        full_path = os.path.join(PROJECT_ROOT, file_path)
        if os.path.exists(full_path):
            try:
                blob_sha = create_blob(full_path)
                file_blobs[file_path] = blob_sha
                if i <= 10:
                    print(f"   [{i}/{len(files_to_push)}] {file_path} ✓")
            except Exception as e:
                print(f"   [{i}/{len(files_to_push)}] {file_path} ✗ {e}")
    print(f"   Created {len(file_blobs)} blobs")

    if not file_blobs:
        print("❌ No blobs created, aborting")
        sys.exit(1)

    # Step 5: Create new tree
    print("4. Creating new tree...")
    new_tree = create_tree(base_tree, file_blobs)
    print(f"   Tree: {new_tree[:7]}")

    # Step 6: Create commit
    print("5. Creating commit...")
    new_commit = create_commit(new_tree, latest_commit, commit_message)
    print(f"   Commit: {new_commit[:7]}")

    # Step 7: Update ref
    print("6. Updating branch ref...")
    result = update_ref(new_commit)
    print(f"   Branch updated: {result['ref']}")

    print("\n" + "=" * 60)
    print("✅ PUSH SUCCESSFUL")
    print(f"   Commit: {new_commit[:7]}")
    print(f"   Files: {len(file_blobs)}")
    print(f"   Vercel deployment should start automatically...")
    print("=" * 60)


if __name__ == "__main__":
    main()
