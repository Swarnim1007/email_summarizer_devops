import os

class Config:
    # Secret key for protecting session data and CSRF tokens
    SECRET_KEY = os.getenv('SECRET_KEY') or 'your_secret_key'

    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:swarnim10@localhost/email_summarizer_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Gmail credentials
    GMAIL_USERNAME = os.getenv('GMAIL_USERNAME')
    GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')
