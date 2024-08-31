import sys
from pathlib import Path
import signal
import os

# Add the project root directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

import time
from utils.logger_config import logger, LOG_DIR
from monitors.website_monitor import monitor_websites
from config.config import MONITOR_FREQUENCY
from utils.email_sender import send_alert_email

def create_log_directory():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
        logger.info(f"Created log directory: {LOG_DIR}")

def signal_handler(signum, frame):
    logger.info("Received signal to terminate. Stopping the service.")
    sys.exit(0)

def create_html_table(results):
    table_html = """
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
            max-width: 800px;
            margin: 20px auto;
            font-family: Arial, sans-serif;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        .status-up {
            color: green;
        }
        .status-down, .status-error {
            color: red;
        }
        .ssl-ok {
            color: green;
        }
        .ssl-expiring {
            color: orange;
        }
        .ssl-error {
            color: red;
        }
    </style>
    <table>
        <tr>
            <th>Website</th>
            <th>Status</th>
            <th>Status Code</th>
            <th>Response Time</th>
            <th>SSL Status</th>
            <th>SSL Days Left</th>
        </tr>
    """
    for result in results:
        status_class = "status-up" if result['status'] == "UP" else "status-down" if result['status'] == "DOWN" else "status-error"
        ssl_class = "ssl-ok" if result['ssl_status'] == "OK" else "ssl-expiring" if "Expiring soon" in result['ssl_status'] else "ssl-error"
        table_html += f"""
        <tr>
            <td>{result['url']}</td>
            <td class="{status_class}">{result['status']}</td>
            <td>{result['status_code']}</td>
            <td>{result['response_time']}s</td>
            <td class="{ssl_class}">{result['ssl_status']}</td>
            <td>{result['ssl_days_left']}</td>
        </tr>
        """
    table_html += "</table>"
    return table_html

def main():
    create_log_directory()
    signal.signal(signal.SIGINT, signal_handler)
    
    logger.info("Starting website monitoring service")
    try:
        while True:
            monitoring_results = monitor_websites()
            if monitoring_results:
                html_table = create_html_table(monitoring_results)
                send_alert_email(html_table)
            time.sleep(MONITOR_FREQUENCY)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
    finally:
        logger.info("Website monitoring service stopped")

if __name__ == "__main__":
    main()
