"""
Configuration settings for the multi-agent chatbot system.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Hugging Face API endpoints and tokens
HF_API_KEY = os.environ.get('HF_API_KEY')

# Agent model endpoints
PROJECT_MANAGER_ENDPOINT = os.environ.get('PROJECT_MANAGER_ENDPOINT', '')
SOFTWARE_ENGINEER_ENDPOINT = os.environ.get('SOFTWARE_ENGINEER_ENDPOINT', '')
DATA_ENGINEER_ENDPOINT = os.environ.get('DATA_ENGINEER_ENDPOINT', '')
QA_TESTER_ENDPOINT = os.environ.get('QA_TESTER_ENDPOINT', '')
DEPLOYMENT_ENGINEER_ENDPOINT = os.environ.get('DEPLOYMENT_ENGINEER_ENDPOINT', '')

# Snowflake database configuration
SF_USER = os.environ.get('SF_USER', '')
SF_PASSWORD = os.environ.get('SF_PASSWORD', '')
SF_ACCOUNT = os.environ.get('SF_ACCOUNT', '')
SF_DATABASE = os.environ.get('SF_DATABASE', '')
SF_SCHEMA = os.environ.get('SF_SCHEMA', '')
SF_WAREHOUSE = os.environ.get('SF_WAREHOUSE', '')

# GitHub configuration
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
GITHUB_REPO = os.environ.get('GITHUB_REPO', '')
GITHUB_BRANCH = os.environ.get('GITHUB_BRANCH', '')

# Database schema for data engineer agent
DATABASE_SCHEMA = """
Tables:
- customers (customer_id, name, email, signup_date, country)
- orders (order_id, customer_id, order_date, total_amount, status)
- products (product_id, name, category, price, in_stock)
- order_items (order_id, product_id, quantity, unit_price)
"""

# Flask application settings
SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(24).hex())
SESSION_LIFETIME = 1800  # 30 minutes session lifetime
