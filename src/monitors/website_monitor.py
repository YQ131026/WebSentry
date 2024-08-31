import requests
from config.config import WEBSITES, SSL_EXPIRY_THRESHOLD, OK_STATUS_CODES  # 修改这行
from utils.logger_config import logger
from checkers.ssl_checker import check_ssl_expiration

def is_status_ok(status_code):
    return status_code in OK_STATUS_CODES

def monitor_websites():
    results = []
    for website in WEBSITES:
        try:
            response = requests.get(website, timeout=10)
            status = "UP" if is_status_ok(response.status_code) else "DOWN"
            response_time = round(response.elapsed.total_seconds(), 2)
            
            ssl_days_left = check_ssl_expiration(website)
            ssl_status = "OK"
            if ssl_days_left is None:
                ssl_status = "ERROR"
            elif ssl_days_left <= SSL_EXPIRY_THRESHOLD:
                ssl_status = f"Expiring soon ({ssl_days_left} days left)"
            
            results.append({
                "url": website,
                "status": status,
                "status_code": response.status_code,
                "response_time": response_time,
                "ssl_status": ssl_status,
                "ssl_days_left": ssl_days_left if ssl_days_left is not None else "N/A"
            })
            logger.info(f"Website {website} is {status} (Code: {response.status_code}). Response time: {response_time}s. SSL: {ssl_status}")
        except requests.RequestException as e:
            results.append({
                "url": website,
                "status": "ERROR",
                "status_code": "N/A",
                "response_time": "N/A",
                "ssl_status": "N/A",
                "ssl_days_left": "N/A"
            })
            logger.error(f"Error monitoring {website}: {str(e)}")
    return results
