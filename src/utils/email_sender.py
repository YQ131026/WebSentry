import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.config import EMAIL_CONFIG
from utils.logger_config import logger

def send_alert_email(html_content):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG['sender']
        msg['To'] = ', '.join(EMAIL_CONFIG['recipients'])
        msg['Subject'] = "Website Monitoring Alert"

        msg.attach(MIMEText(html_content, 'html'))

        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['username'], EMAIL_CONFIG['password'])
            server.send_message(msg)
        
        logger.info("Alert email sent successfully")
    except Exception as e:
        logger.error(f"Failed to send alert email: {str(e)}")
