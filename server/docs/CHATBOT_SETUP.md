# Google Calendar Setup Guide

This guide will help you set up Google Calendar integration for the AI Calendar Assistant.

## Prerequisites

1. Google Cloud Account
2. Python 3.7 or higher
3. OpenAI API key

## Setup Steps

### 1. Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Note your Project ID

### 2. Enable Google Calendar API

1. Go to [API Library](https://console.cloud.google.com/apis/library)
2. Search for "Google Calendar API"
3. Click "Enable"

### 3. Configure OAuth Consent Screen

1. Go to [OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent)
2. Select "External" user type
3. Fill in required information:
   - App name: "AI Calendar Assistant"
   - User support email
   - Developer contact information
4. Add scopes:
   - `./auth/calendar`
   - `./auth/calendar.events`
   - `./auth/calendar.readonly`
5. Add test users (your Google account email)

### 4. Create OAuth 2.0 Credentials

1. Go to [Credentials](https://console.cloud.google.com/apis/credentials)
2. Click "Create Credentials" > "OAuth client ID"
3. Select "Desktop app"
4. Name: "AI Calendar Assistant"
5. Download the credentials file
6. Rename to `credentials.json`
7. Place in `config/` directory

### 5. First Run Authentication

1. Run the application
2. Browser will open for Google authentication
3. Select your Google account
4. Grant permissions
5. Token will be saved as `token.json`

## Troubleshooting

### Common Issues

1. "Invalid client" error:
   - Check credentials.json is correctly placed
   - Verify OAuth consent screen is configured

2. "Access denied" error:
   - Ensure your email is added as a test user
   - Check required scopes are enabled

3. Token refresh issues:
   - Delete token.json and re-authenticate
   - Check your internet connection

## Security Notes

1. Keep credentials.json secure
2. Never commit credentials to version control
3. Use environment variables for sensitive data
4. Regularly rotate OAuth client secrets

## Additional Resources

- [Google Calendar API Documentation](https://developers.google.com/calendar/api/guides/overview)
- [OAuth 2.0 for Desktop Apps](https://developers.google.com/identity/protocols/oauth2/native-app) 