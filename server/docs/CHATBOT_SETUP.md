# Calendar GPT Chatbot Setup Guide

## Prerequisites

1. **Python Environment**
   - Python 3.7 or higher
   - Virtual environment (venv)

2. **API Keys**
   - OpenAI API key (for GPT integration)
   - Google Calendar API credentials

## Setup Steps

### 1. Virtual Environment

```bash
# Navigate to server directory
cd server

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
# Make sure your virtual environment is activated
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. OpenAI API Setup

1. Get your API key:
   - Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
   - Create a new API key
   - Copy the key

2. Set up billing (required):
   - Go to [OpenAI Billing](https://platform.openai.com/account/billing)
   - Add a payment method
   - Set usage limits (optional)

3. Create `.env` file in the server directory:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

### 4. Google Calendar Setup

1. Get Google Calendar credentials:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project or select existing one
   - Enable Google Calendar API
   - Create OAuth 2.0 credentials (Desktop application)
   - Download credentials and save as `credentials.json` in the server directory

2. First-time authentication:
   - Run the chatbot
   - Follow OAuth flow in browser
   - Grant necessary permissions
   - Token will be saved as `token.json`

## Running the Chatbot

1. Make sure you're in the server directory with activated virtual environment
2. Run the chatbot:
   ```bash
   python calendar_chatbot_gpt.py
   ```

## Available Commands

### 1. Schedule Events
```
"Schedule a team meeting tomorrow at 2 PM for 1 hour"
"Create a dentist appointment on 2024-01-25 at 10:00 for 30 minutes"
```

### 2. Show Events
```
"What's on my calendar today?"
"Show me my meetings for this week"
"What events do I have tomorrow?"
```

### 3. Find Available Slots
```
"When am I free tomorrow?"
"Find me a 30-minute slot for tomorrow"
"What time slots are available next Monday?"
```

### 4. Update Events
```
"Update event abc123 title to 'Updated Meeting'"
"Change the time of event xyz789 to tomorrow at 3 PM"
```

### 5. Delete Events
```
"Delete event abc123"
"Cancel the meeting with ID xyz789"
```

## Troubleshooting

### Common Issues

1. **OpenAI API Key Issues**
   - Error: "OpenAI API key not found"
   - Solution: Check .env file and key validity

2. **Google Calendar Authentication**
   - Error: "credentials.json not found"
   - Solution: Download and place credentials file correctly

3. **Token Expiration**
   - Error: "Token has expired"
   - Solution: Delete token.json and re-authenticate

4. **Virtual Environment**
   - Error: "Module not found"
   - Solution: Ensure venv is activated and dependencies installed

### Debug Mode

For detailed error messages, you can enable debug mode:
```python
DEBUG=True python calendar_chatbot_gpt.py
```

## Security Notes

1. **API Keys**
   - Never commit API keys to version control
   - Keep .env file secure
   - Rotate keys periodically

2. **Google Calendar Access**
   - Review and limit OAuth scopes
   - Regularly check authorized applications
   - Use separate test calendar for development

3. **Data Storage**
   - token.json contains sensitive data
   - Keep credentials.json secure
   - Add both to .gitignore

## Best Practices

1. **Command Format**
   - Be specific with times and dates
   - Use clear event titles
   - Specify duration when scheduling

2. **Calendar Management**
   - Check for conflicts before scheduling
   - Use descriptive event titles
   - Add location and description when relevant

3. **Error Handling**
   - Check error messages
   - Verify input format
   - Use help command when needed

## Support

For issues and questions:
1. Check troubleshooting section
2. Review error messages
3. Verify configuration
4. Check API documentation:
   - [OpenAI API](https://platform.openai.com/docs)
   - [Google Calendar API](https://developers.google.com/calendar) 