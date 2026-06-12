# SQL SET UP, more companies could be added

from dotenv import load_dotenv
import os

load_dotenv()

COMPANIES = ["examples"]

DB_CONFIG = {
    "host":     os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user":     os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port":     int(os.getenv("DB_PORT", 5432))
}
