import smtplib
from email.mime.text import MIMEText
from email.header import Header

SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 465
SMTP_USER = "840754587@qq.com"
SMTP_PASS = "rkphxyrugwvabdbf"
FROM_EMAIL = "840754587@qq.com"
TO_EMAIL = "840754587@qq.com"

msg = MIMEText("这是一封测试邮件，验证邮件通知功能是否正常。", "plain", "utf-8")
msg["From"] = FROM_EMAIL
msg["To"] = TO_EMAIL
msg["Subject"] = Header("【测试】AIToolCrux邮件通知测试", "utf-8")

try:
    server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, local_hostname="localhost")
    server.login(SMTP_USER, SMTP_PASS)
    server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
    server.quit()
    print("✅ 测试邮件发送成功！请检查邮箱。")
except Exception as e:
    print(f"❌ 发送失败: {e}")
