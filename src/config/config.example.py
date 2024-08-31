# Email configuration
EMAIL_CONFIG = {
    'smtp_server': 'smtp.example.com',
    'smtp_port': 587,
    'username': 'your_email@example.com',
    'password': 'your_email_password',
    'sender': 'sender@example.com',
    'recipients': ['recipient1@example.com', 'recipient2@example.com']
}

# List of websites to monitor
WEBSITES = [
    "https://www.example1.com",
    "https://www.example2.com",
    "https://api.example3.com",
    # Add more websites as needed
]

# Request timeout in seconds
REQUEST_TIMEOUT = 10

# Monitor frequency in seconds
MONITOR_FREQUENCY = 5

# Status codes considered as OK
OK_STATUS_CODES = [200, 301, 302, 401]

# SSL configuration
SSL_EXPIRY_THRESHOLD = 30  # Days before expiry to start warning

# SSL verification
VERIFY_SSL = False  # Set to True in production with proper cert chain

# Log file path
LOG_FILE_PATH = "logs/monitor.log"
