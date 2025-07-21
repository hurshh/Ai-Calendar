# AI Calendar Assistant

An intelligent calendar management system that provides a powerful interface for Google Calendar operations through both CLI and assistant-based interactions.

## Features

- 🔐 Secure OAuth 2.0 authentication with Google Calendar API
- 📅 Comprehensive calendar management
- ⚡ Event creation, deletion, and updates
- 🔍 Smart availability checking and conflict detection
- 📊 Free/busy information retrieval
- 🤖 AI-powered calendar assistant
- 💻 Command-line interface

## Project Structure

```
ai-cal/
├── server/
│   ├── calendar_assistant.py  # AI assistant interface
│   ├── calendar_cli.py       # Command-line interface
│   ├── calendar_handler.py   # Core calendar operations
│   └── requirements.txt      # Python dependencies
└── client/
    └── calendar_handler.py   # Client-side handler
```

## Prerequisites

- Python 3.7+
- Google Cloud Console Project with Calendar API enabled
- OAuth 2.0 credentials for Google Calendar API

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/hurshh/Ai-Calendar.git
   cd ai-cal/server
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up Google Calendar API:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable Google Calendar API
   - Create OAuth 2.0 credentials (Desktop application)
   - Download credentials and save as `credentials.json` in the client directory

## Usage

### Command Line Interface

```bash
# Run the CLI
python calendar_cli.py

# Available commands:
- list    : List all calendars
- events  : Show upcoming events
- add     : Add new event
- delete  : Delete event
- update  : Update event details
- check   : Check availability
- find    : Find available slots
```

### AI Assistant Interface

```bash
# Run the AI assistant
python calendar_assistant.py

# Example interactions:
- "Schedule a team meeting for tomorrow at 2 PM"
- "Show my calendar for next week"
- "Find a free 1-hour slot this afternoon"
- "Update the meeting with John to Friday"
```

### Calendar Handler API

```python
from calendar_handler import CalendarHandler

# Initialize and authenticate
handler = CalendarHandler()
handler.authenticate()

# Get calendars
calendars = handler.get_calendars()

# Add event
event_id = handler.add_event(
    title="Team Meeting",
    start_time="2024-01-20T14:00:00",
    duration_minutes=60,
    description="Weekly team sync",
    attendees=["team@company.com"]
)

# Check availability
is_available, conflicts = handler.check_availability(
    start_time="2024-01-20T14:00:00",
    end_time="2024-01-20T15:00:00"
)
```

## Security Notes

- Store `credentials.json` and `token.json` securely
- Never commit these files to version control
- Use environment variables for sensitive data
- Regularly rotate OAuth 2.0 credentials

## Dependencies

- google-auth==2.23.4
- google-auth-oauthlib==1.1.0
- google-auth-httplib2==0.1.1
- google-api-python-client==2.108.0
- pytz==2023.3

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is provided as-is for educational and development purposes.

## Author

Harsh Pandey

## Acknowledgments

- Google Calendar API Documentation
- Python Google API Client Library 