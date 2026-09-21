#!/usr/bin/env python3
"""Uptime monitor: check if aitoolcrux.com is up. Send email only if down.
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
USER_AGENT = "Mozilla/5.0 (compatible; AIToolCrux-UptimeBot/1.0)"


def send_alert(email_user: str, auth_code: str, error_msg: str):
    """Send alert email via QQ SMTP. Logs but does not exit on failure."""
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
        # Email failure should NOT mark the uptime check as failed
        print(f"⚠️ Failed to send alert email (non-fatal): {e}")


def main():
    email_user = os.environ.get("QQ_MAIL_USER", "")
    auth_code = os.environ.get("QQ_MAIL_AUTH_CODE", "")

    print(f"Checking uptime: {SITE_URL}")
    req = Request(SITE_URL, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(req, timeout=15) as resp:
            status = resp.getcode()
        if status in EXPECTED_STATUS:
            print(f"✅ Site is UP (HTTP {status})")
            return
        else:
            error = f"HTTP {status} (expected 200 or 308)"
            print(f"❌ Site DOWN: {error}")
            if email_user and auth_code:
                send_alert(email_user, auth_code, error)
            else:
                print("⚠️ No email credentials configured, skipping alert")
    except HTTPError as e:
        error = f"HTTP {e.code} (expected 200 or 308)"
        print(f"❌ Site DOWN: {error}")
        if email_user and auth_code:
            send_alert(email_user, auth_code, error)
        else:
            print("⚠️ No email credentials configured, skipping alert")
    except URLError as e:
        error = f"Connection error: {e.reason}"
        print(f"❌ Site DOWN: {error}")
        if email_user and auth_code:
            send_alert(email_user, auth_code, error)
        else:
            print("⚠️ No email credentials configured, skipping alert")
    except Exception as e:
        error = f"Unexpected error: {e}"
        print(f"❌ Site DOWN: {error}")
        if email_user and auth_code:
            send_alert(email_user, auth_code, error)
        else:
            print("⚠️ No email credentials configured, skipping alert")


if __name__ == "__main__":
    main()
