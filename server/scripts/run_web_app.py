#!/usr/bin/env python3

import os
import sys
from pathlib import Path

def check_requirements():
    """Check if all requirements are installed"""
    try:
        import flask
        import flask_cors
        import openai
        import dotenv
        print("✓ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("\nPlease install requirements:")
        print("pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_path = Path('./config/.env')  # Look for .env in config directory relative to server
    if not env_path.exists():
        print("✗ .env file not found in config directory")
        print("\nPlease create a .env file in config/ with:")
        print("OPENAI_API_KEY=your-openai-api-key-here")
        print("\nGet your API key from: https://platform.openai.com/api-keys")
        return False
    
    # Load and check environment variables
    from dotenv import load_dotenv
    load_dotenv(env_path)
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("✗ OPENAI_API_KEY not found in .env file")
        print("\nPlease add to your .env file:")
        print("OPENAI_API_KEY=your-openai-api-key-here")
        return False
    
    print("✓ Environment configuration found")
    return True

def check_google_credentials():
    """Check if Google Calendar credentials are set up"""
    creds_file = Path('./config/credentials.json')  # Look for credentials in config directory
    if not creds_file.exists():
        print("⚠ Google Calendar credentials.json not found")
        print("Calendar functionality may not work properly")
        print("See docs/CHATBOT_SETUP.md for Google Calendar setup instructions")
        return False
    
    print("✓ Google Calendar credentials found")
    return True

def main():
    print("🗓️ AI Calendar Web App Setup Check")
    print("=" * 50)
    
    # Check all requirements
    all_checks_passed = True
    
    if not check_requirements():
        all_checks_passed = False
    
    if not check_env_file():
        all_checks_passed = False
    
    if not check_google_credentials():
        print("Note: You can still test the app without Google Calendar")
    
    if not all_checks_passed:
        print("\n❌ Some requirements are missing. Please fix the above issues.")
        sys.exit(1)
    
    print("\n✅ All checks passed! Starting the web application...")
    print("\n🌐 Access the app at: http://localhost:5001")
    print("📱 The app is mobile-responsive!")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    # Add server directory to Python path
    server_dir = str(Path(__file__).parent.parent.absolute())
    sys.path.insert(0, server_dir)
    
    # Import and run the web app
    try:
        from api.web_app import app
        app.run(debug=True, host='0.0.0.0', port=5001)
    except Exception as e:
        print(f"\n❌ Error starting web app: {e}")
        print("Please check the error messages above for troubleshooting")

if __name__ == "__main__":
    main() 