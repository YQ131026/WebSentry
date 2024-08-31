import json
import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from config.config import LOG_FILE_PATH

# 定义 LOG_DIR
LOG_DIR = 'logs'

# 确保日志目录存在
os.makedirs(LOG_DIR, exist_ok=True)

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, "%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }
        if hasattr(record, 'results'):
            log_record['results'] = record.results
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_record, indent=2, ensure_ascii=False)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

try:
    log_dir = os.path.dirname(LOG_FILE_PATH)
    os.makedirs(log_dir, exist_ok=True)
    print(f"尝试创建日志目录: {log_dir}")
    
    if not os.path.exists(log_dir):
        print(f"无法创建日志目录: {log_dir}")
        print(f"当前工作目录: {os.getcwd()}")
        print(f"目录权限: {oct(os.stat(os.path.dirname(log_dir)).st_mode)[-3:]}")
        sys.exit(1)
    
    file_handler = RotatingFileHandler(LOG_FILE_PATH, maxBytes=10*1024*1024, backupCount=5)
    print(f"成功创建日志文件处理器: {LOG_FILE_PATH}")
except Exception as e:
    print(f"设置日志时发生错误: {str(e)}")
    print(f"当前工作目录: {os.getcwd()}")
    print(f"LOG_FILE_PATH: {LOG_FILE_PATH}")
    print(f"用户: {os.getlogin()}")
    print(f"有效用户ID: {os.geteuid()}")
    sys.exit(1)

console_handler = logging.StreamHandler()
console_handler.setFormatter(JsonFormatter())
logger.addHandler(console_handler)

# 确保 LOG_DIR 被导出
__all__ = ['logger', 'LOG_DIR']
