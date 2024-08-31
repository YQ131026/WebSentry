# Email configuration
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
SENDER_EMAIL = "sender@example.com"
SENDER_PASSWORD = "your_password_here"
RECIPIENT_EMAIL = "recipient1@example.com,recipient2@example.com"

# List of websites to monitor
WEBSITES = [
    "https://example1.com",
    "https://example2.com",
    # Add more websites here
]

# Request timeout in seconds
REQUEST_TIMEOUT = 10

# Monitor frequency in seconds
MONITOR_FREQUENCY = 5

# Status code configurations
STATUS_CODES = {
    200: "OK",
    300: "Warning",
    400: "Client Error",
    500: "Server Error",
    502: "Bad Gateway",
    504: "Gateway Timeout"
}

# Status codes that trigger alerts
ALERT_STATUS_CODES = [300, 400, 500, 502, 504]

# Status codes to exclude from alerts
EXCLUDED_ALERT_STATUS_CODES = [200, 301, 401]

# Number of days before certificate expiration to trigger a warning
CERTIFICATE_WARNING_DAYS = 7

# SSL verification
VERIFY_SSL = False  # Set to True in production with proper cert chain

# Log file path
LOG_FILE_PATH = "logs/monitor.log"
