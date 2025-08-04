"""
Server configuration settings
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# OpenAI settings
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = "gpt-3.5-turbo"

# Google Calendar settings
GOOGLE_CREDENTIALS_FILE = 'credentials.json'
GOOGLE_TOKEN_FILE = 'token.json'
GOOGLE_CALENDAR_SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events'
]

# Server settings
DEBUG = True
HOST = '0.0.0.0'
PORT = 5001

# Default timezone (will be overridden by system timezone)
DEFAULT_TIMEZONE = 'UTC'

# Calendar settings
DEFAULT_CALENDAR_ID = 'primary'
DEFAULT_EVENT_DURATION = 60  # minutes
WORKING_HOURS = {
    'start': 9,  # 9 AM
    'end': 17    # 5 PM
}

# API endpoints
API_PREFIX = '/api'
ENDPOINTS = {
    'events': f'{API_PREFIX}/events',
    'chat': f'{API_PREFIX}/chat',
    'refresh': f'{API_PREFIX}/refresh'
} 