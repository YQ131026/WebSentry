import subprocess
import re
import time
from utils.logger_config import logger
from config.config import REQUEST_TIMEOUT, VERIFY_SSL
import urllib3

# Disable the InsecureRequestWarning if VERIFY_SSL is False
if not VERIFY_SSL:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_ssl_expiration(url, retries=3, delay=2):
    for attempt in range(retries):
        try:
            cmd = f"curl -vI --max-time {REQUEST_TIMEOUT} {url} 2>&1 | grep 'expire date'"
            output = subprocess.check_output(cmd, shell=True, universal_newlines=True).strip()
            
            match = re.search(r'date:\s+(.+)', output)
            if match:
                date_str = match.group(1)
                expire_timestamp = int(time.mktime(time.strptime(date_str, "%b %d %H:%M:%S %Y %Z")))
                current_timestamp = int(time.time())
                
                days_left = (expire_timestamp - current_timestamp) // (24 * 3600)
                return days_left
            else:
                logger.warning(f"Unable to extract date from curl output for {url} (Attempt {attempt + 1}/{retries})")
        except subprocess.CalledProcessError:
            logger.warning(f"Unable to fetch SSL information for {url} (Attempt {attempt + 1}/{retries})")
        except Exception as e:
            logger.error(f"Error checking SSL for {url}: {str(e)} (Attempt {attempt + 1}/{retries})")
        
        if attempt < retries - 1:
            time.sleep(delay)
    
    return None
