import sys
from pathlib import Path
import signal
import os
from utils.ai_summarizer import summarize_results
import json
from config.config import EMAIL_CONFIG, AI_CONFIG

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

def check_config():
    if 'enabled' not in EMAIL_CONFIG:
        raise KeyError("EMAIL_CONFIG 中缺少 'enabled' 键")
    if 'enabled' not in AI_CONFIG:
        raise KeyError("AI_CONFIG 中缺少 'enabled' 键")

def main():
    try:
        check_config()  # 在主循环开始前检查配置
        create_log_directory()
        signal.signal(signal.SIGINT, signal_handler)
        
        logger.info("Starting website monitoring service")
        while True:
            monitoring_results = monitor_websites()
            if monitoring_results:
                # 创建 HTML 表格
                html_table = create_html_table(monitoring_results)
                
                # 获取 AI 总结
                results_json = json.dumps(monitoring_results, indent=2)
                ai_summary = summarize_results(results_json)
                
                if ai_summary:
                    logger.info(f"AI 总结结果:\n{ai_summary}")
                    print(f"AI 总结结果:\n{ai_summary}")
                else:
                    logger.warning("未能获取 AI 总结")
                
                # 构建邮件内容
                email_content = f"<h2>监控结果</h2>\n{html_table}\n\n"
                if ai_summary:
                    email_content += f"<h2>AI 总结</h2>\n<pre>{ai_summary}</pre>"
                
                # 发送报警邮件
                send_alert_email(email_content)
            
            time.sleep(MONITOR_FREQUENCY)
    except KeyError as e:
        logger.error(f"配置错误: {str(e)}")
    except Exception as e:
        logger.error(f"发生意外错误: {str(e)}")
    finally:
        logger.info("网站监控服务已停止")

if __name__ == "__main__":
    main()
