"""
发布器 - 自动写入posts.json + git提交 + 线上验证
调用: python scripts/seo_toolkit/publisher.py --slug {文章slug} --message "commit message"
输出: commit hash + 线上验证结果

整合工具:
- Python JSON操作
- git命令
- Vercel部署等待
- HTTP验证
"""
import sys, os, json, argparse, time, subprocess, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import *

def run_git(args, cwd=PROJECT_ROOT):
    """运行git命令"""
    env = os.environ.copy()
    env["HTTP_PROXY"] = GIT_PROXY
    env["HTTPS_PROXY"] = GIT_PROXY
    result = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True, env=env, timeout=60)
    return result.returncode, result.stdout, result.stderr

def tsc_check():
    """TypeScript检查"""
    result = subprocess.run(["npx", "tsc", "--noEmit"], cwd=PROJECT_ROOT,
                          capture_output=True, text=True, timeout=120)
    return result.returncode == 0, result.stdout + result.stderr

def commit_and_push(message, files=None):
    """git add + commit + pull --rebase + push"""
    if files:
        code, out, err = run_git(["add"] + files)
    else:
        code, out, err = run_git(["add", "-A"])
    if code != 0:
        return False, f"git add失败: {err}"

    code, out, err = run_git(["commit", "-m", message])
    if code != 0:
        return False, f"git commit失败: {err}"

    code, out, err = run_git(["pull", "--rebase"])
    if code != 0:
        return False, f"git pull失败: {err}"

    code, out, err = run_git(["push"])
    if code != 0:
        return False, f"git push失败: {err}"

    # 获取commit hash
    code, out, err = run_git(["rev-parse", "HEAD"])
    commit_hash = out.strip() if code == 0 else "unknown"
    return True, commit_hash

def verify_online(slug, max_wait=180):
    """等待Vercel部署并验证线上"""
    url = f"https://www.aitoolcrux.com/blog/{slug}"
    print(f"  等待Vercel部署（最多{max_wait}秒）...")
    for i in range(max_wait // 15):
        time.sleep(15)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            resp = urllib.request.urlopen(req, timeout=10)
            if resp.status == 200:
                content = resp.read().decode("utf-8", errors="ignore")
                if len(content) > 5000 and "404" not in content[:500]:
                    return True, f"HTTP 200, 内容长度{len(content)}"
        except Exception as e:
            pass
        print(f"    等待中... ({(i+1)*15}s)")
    return False, "部署超时或页面未上线"

def update_state(slug, status="completed"):
    """更新state.json中对应待办状态"""
    with open(STATE_JSON, "r", encoding="utf-8") as f:
        state = json.load(f)
    updated = 0
    for task in state.get("next_iteration_focus", []):
        if slug in task.get("task", "") and task.get("status") == "pending":
            task["status"] = status
            task["completed_at"] = time.strftime("%Y-%m-%d")
            updated += 1
    with open(STATE_JSON, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    return updated

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", required=True, help="文章slug")
    parser.add_argument("--message", default="feat(content): add new article", help="commit message")
    parser.add_argument("--no-verify", action="store_true", help="跳过线上验证")
    args = parser.parse_args()

    print(f"=== 发布器 ===")
    print(f"文章: {args.slug}")

    # Step 1: 确认文章存在
    with open(POSTS_JSON, "r", encoding="utf-8") as f:
        posts = json.load(f)
    post = next((p for p in posts if p.get("slug") == args.slug), None)
    if not post:
        print(f"[ERROR] 未找到文章: {args.slug}")
        sys.exit(1)
    print(f"标题: {post.get('title','')}")
    print(f"字数: {len(post.get('content','').split())}")

    # Step 2: tsc检查
    print("\n[1/4] TypeScript检查...")
    ok, output = tsc_check()
    if not ok:
        print(f"❌ tsc失败:\n{output[:500]}")
        sys.exit(1)
    print("  ✅ tsc通过")

    # Step 3: git提交
    print("\n[2/4] Git提交...")
    files = ["data/posts.json"]
    screenshot_dir = os.path.join(SCREENSHOTS_DIR, args.slug)
    if os.path.exists(screenshot_dir):
        files.append(f"public/screenshots/{args.slug}/")
    ok, result = commit_and_push(args.message, files)
    if not ok:
        print(f"❌ {result}")
        sys.exit(1)
    print(f"  ✅ 已推送: {result}")

    # Step 4: 线上验证
    if not args.no_verify:
        print("\n[3/4] 线上验证...")
        ok, result = verify_online(args.slug)
        if not ok:
            print(f"⚠️  {result}")
        else:
            print(f"  ✅ {result}")

    # Step 5: 更新state.json
    print("\n[4/4] 更新state.json...")
    updated = update_state(args.slug)
    print(f"  ✅ 更新了 {updated} 条待办状态")

    print(f"\n=== 发布完成 ===")
    print(f"Commit: {result if isinstance(result, str) and len(result)<20 else '已推送'}")
    print(f"文章URL: https://www.aitoolcrux.com/blog/{args.slug}")

if __name__ == "__main__":
    main()
