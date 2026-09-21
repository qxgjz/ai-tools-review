#!/usr/bin/env python3
"""Uptime monitor: check if aitoolcrux.com is up. Send email only if down.
Uses only Python stdlib (urllib/smtplib) so no pip install needed in CI.
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
TIMEOUT = 15


def send_alert(email_user: str, auth_code: str, error_msg: str):
    """Send alert email via QQ SMTP."""
    msg = MIMEMultipart()
    msg["From"] = email_user
    msg["To"] = email_user
    msg["Subject"] = "⚠️ 网站宕机告警 - AIToolCrux"

    body = f"""
    <html><body>
    <h2 style="color:red;">⚠️ 网站宕机告警</h2>
    <p><strong>网站：</strong>{SITE_URL}</p>
    <p><strong>时间：</strong>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p><strong>错误：</strong>{error_msg}</p>
    <p>请立即检查Vercel部署状态！</p>
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
        print(f"❌ Failed to send email: {e}")
        sys.exit(1)


def check_site():
    """Return (ok, status_or_error). urllib follows redirects by default."""
    req = Request(SITE_URL, headers={"User-Agent": "UptimeMonitor/1.0"})
    try:
        with urlopen(req, timeout=TIMEOUT) as resp:
            return True, resp.status
    except HTTPError as e:
        # e.g. 404/500, but redirects already followed
        if e.code in EXPECTED_STATUS:
            return True, e.code
        return False, f"HTTP {e.code}"
    except URLError as e:
        return False, f"Connection error: {e.reason}"
    except Exception as e:
        return False, f"Unexpected error: {e}"


def main():
    email_user = os.environ.get("QQ_MAIL_USER", "")
    auth_code = os.environ.get("QQ_MAIL_AUTH_CODE", "")

    print(f"Checking uptime: {SITE_URL}")
    ok, info = check_site()
    if ok:
        print(f"✅ Site is UP (HTTP {info})")
        return

    error = str(info)
    print(f"❌ Site DOWN: {error}")
    if email_user and auth_code:
        send_alert(email_user, auth_code, error)
    else:
        print("⚠️ No email credentials configured, skipping alert")


if __name__ == "__main__":
    main()
