from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.config.config import EMAIL_CONFIG
from src.utils.logger_config import logger
import smtplib

def send_alert_email(content):
    if 'enabled' not in EMAIL_CONFIG:
        logger.error("EMAIL_CONFIG 中缺少 'enabled' 键")
        return
    if not EMAIL_CONFIG['enabled']:
        logger.info("邮件报警功能未启用")
        return

    msg = MIMEMultipart()
    msg['Subject'] = "网站监控报警"
    msg['From'] = EMAIL_CONFIG['sender_email']
    msg['To'] = ", ".join(EMAIL_CONFIG['recipient_emails'])

    html_part = MIMEText(content, 'html')
    msg.attach(html_part)

    try:
        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            if EMAIL_CONFIG['use_tls']:
                server.starttls()
            server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
            server.send_message(msg)
        logger.info("报警邮件发送成功")
    except Exception as e:
        logger.error(f"发送报警邮件时出错: {str(e)}")
