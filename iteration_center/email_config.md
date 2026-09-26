# AIToolCrux Email Config

## SMTP Settings
- SMTP_SERVER: smtp.qq.com
- SMTP_PORT: 465
- SMTP_USER: 840754587@qq.com
- SMTP_PASS: rkphxyrugwvabdbf
- FROM_EMAIL: 840754587@qq.com
- TO_EMAIL: 840754587@qq.com
- ENABLED: true

## IMPORTANT: Windows Fix
When using Python smtplib on Windows, MUST set local_hostname="localhost"
to avoid UnicodeEncodeError caused by Chinese computer name.

Correct code:
server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, local_hostname="localhost")

## Usage
Daily report will be sent to this email every day at 21:30.
