import os

MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "plagiarismguard")
MYSQL_USER = os.getenv("MYSQL_USER", "pg_user")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "pg_password")
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672//")
