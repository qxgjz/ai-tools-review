#!/usr/bin/env python3
"""Uptime + content integrity monitor for aitoolcrux.com.
Checks HTTP status AND that key pages actually render expected content.
Sends alert email only if down or content missing.
Uses only Python stdlib (urllib) — no pip dependencies needed on CI runner.
"""
import os
import smtplib
import sys
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

SITE_URL = "https://www.aitoolcrux.com"
EXPECTED_STATUS = {200, 308}
QQ_SMTP_SERVER = "smtp.qq.com"
QQ_SMTP_PORT = 465
USER_AGENT = "Mozilla/5.0 (compatible; AIToolCrux-UptimeBot/2.0)"

# Pages to check: (path, list of required content markers)
# Markers must be specific to article BODY content, not just title/TOC
# If any marker is missing, alert fires
CONTENT_CHECKS = [
    ("/", ["aitoolcrux", "AI", "tool"]),
    # Blog article — must have actual body content (not just title/TOC)
    # "best AI search engine" only appears in article body, not in title or TOC
    ("/blog/perplexity-ai-review-2026", ["best AI search engine", "Key Takeaways", "Conclusion First"]),
    # Tool detail page
    ("/tools/perplexity-ai", ["Perplexity", "AI"]),
    # Blog listing
    ("/blog", ["blog", "article"]),
]


def fetch_page(path: str, timeout: int = 30) -> tuple[int, str]:
    """Fetch a page, return (status_code, html_content)."""
    url = SITE_URL + path
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=timeout) as resp:
        status = resp.getcode()
        # Read up to 500KB — enough for content checks without memory issues
        html = resp.read(500_000).decode("utf-8", errors="replace")
    return status, html


def check_content(path: str, markers: list[str]) -> tuple[bool, str]:
    """Check that page returns 200 and contains all required markers."""
    try:
        status, html = fetch_page(path)
    except HTTPError as e:
        return False, f"HTTP {e.code} on {path}"
    except URLError as e:
        return False, f"Connection error on {path}: {e.reason}"
    except Exception as e:
        return False, f"Unexpected error on {path}: {e}"

    if status not in EXPECTED_STATUS:
        return False, f"HTTP {status} on {path} (expected 200/308)"

    missing = [m for m in markers if m.lower() not in html.lower()]
    if missing:
        return False, f"Content missing on {path}: {', '.join(missing)} (page size: {len(html)} bytes)"

    return True, f"OK {path} ({len(html)} bytes, all markers found)"


def send_alert(email_user: str, auth_code: str, error_msg: str):
    """Send alert email via QQ SMTP. Logs but does not exit on failure."""
    msg = MIMEMultipart()
    msg["From"] = email_user
    msg["To"] = email_user
    msg["Subject"] = "⚠️ 网站异常告警 - AIToolCrux"

    body = f"""
    <html><body>
    <h2 style="color:red;">⚠️ 网站异常告警</h2>
    <p><strong>网站：</strong>{SITE_URL}</p>
    <p><strong>时间：</strong>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p><strong>问题：</strong></p>
    <pre style="background:#f5f5f5;padding:10px;border-radius:4px;">{error_msg}</pre>
    <p>请立即检查Vercel部署状态和最近的代码提交！</p>
    </body></html>
    """
    msg.attach(MIMEText(body, "html", "utf-8"))

    try:
        server = smtplib.SMTP_SSL(QQ_SMTP_SERVER, QQ_SMTP_PORT, timeout=15)
        server.login(email_user, auth_code)
        server.sendmail(email_user, email_user, msg.as_string())
        server.quit()
        print(f"✅ Alert email sent to {email_user}")
    except Exception as e:
        print(f"⚠️ Failed to send alert email (non-fatal): {e}")


def main():
    email_user = os.environ.get("QQ_MAIL_USER", "")
    auth_code = os.environ.get("QQ_MAIL_AUTH_CODE", "")

    all_ok = True
    all_results = []

    for path, markers in CONTENT_CHECKS:
        ok, msg = check_content(path, markers)
        all_results.append(msg)
        if not ok:
            all_ok = False
            print(f"❌ {msg}")
        else:
            print(f"✅ {msg}")

    if all_ok:
        print(f"\n✅ All {len(CONTENT_CHECKS)} pages passed content integrity check")
        return

    error_summary = "\n".join(all_results)
    print(f"\n❌ Content integrity check FAILED:\n{error_summary}")

    if email_user and auth_code:
        send_alert(email_user, auth_code, error_summary)
    else:
        print("⚠️ No email credentials configured, skipping alert")

    # Exit with non-zero so GitHub Actions marks the run as failed
    sys.exit(1)


if __name__ == "__main__":
    main()
