# Calendar Handler Setup Guide

## Initial Setup

### 1. Virtual Environment Setup
```bash
# Navigate to the server directory
cd server

# Create a new virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Verify activation (should show virtual environment path)
which python
```

### 2. Install Dependencies
```bash
# Make sure your virtual environment is activated
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Google Calendar API Setup

1. **Create Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Note down your Project ID

2. **Enable Google Calendar API**:
   - In Google Cloud Console, go to "APIs & Services" > "Library"
   - Search for "Google Calendar API"
   - Click "Enable"

3. **Configure OAuth Consent Screen**:
   - Go to "APIs & Services" > "OAuth consent screen"
   - Choose "External" user type
   - Fill in required information:
     - App name
     - User support email
     - Developer contact email
   - Add scopes:
     - `./auth/calendar.readonly`
     - `./auth/calendar.events`
     - `./auth/calendar`
   - Add test users (your Google email)

4. **Create OAuth 2.0 Credentials**:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop application"
   - Name your client
   - Download the client configuration file
   - Rename it to `credentials.json`
   - Place it in the `server` directory

## Usage Guide

### 1. Authentication

```python
from calendar_handler import CalendarHandler

# Initialize handler
handler = CalendarHandler()

# Authenticate (will open browser for OAuth flow)
handler.authenticate()
```

### 2. Calendar Operations

#### List All Calendars
```python
# Get all calendars
calendars = handler.get_calendars()

# Print calendar details
for calendar in calendars:
    print(f"Calendar: {calendar['summary']}")
    print(f"ID: {calendar['id']}")
```

#### Event Management

```python
# Add new event
event = handler.add_event(
    title="Team Meeting",
    start_time="2024-01-20T14:00:00",
    duration_minutes=60,
    description="Weekly team sync",
    attendees=["team@example.com"],
    location="Conference Room A"
)

# Update event
handler.update_event(
    event_id="event_id_here",
    title="Updated Team Meeting",
    start_time="2024-01-21T15:00:00",
    duration_minutes=90
)

# Delete event
handler.delete_event(event_id="event_id_here")

# Get events for a time range
events = handler.get_events(
    start_time="2024-01-20T00:00:00",
    end_time="2024-01-21T00:00:00"
)
```

#### Availability Checking

```python
# Check specific time slot
is_available, conflicts = handler.check_availability(
    start_time="2024-01-20T14:00:00",
    end_time="2024-01-20T15:00:00"
)

# Find available slots
available_slots = handler.find_available_slots(
    date="2024-01-20",
    duration_minutes=60,
    start_hour=9,
    end_hour=17
)
```

### 3. Error Handling

```python
try:
    handler.add_event(...)
except CalendarException as e:
    print(f"Calendar operation failed: {e}")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
```

## Security Best Practices

1. **Credential Management**:
   - Never commit `credentials.json` or `token.json` to version control
   - Add these files to `.gitignore`
   - Regularly rotate OAuth 2.0 credentials
   - Use environment variables for sensitive data

2. **Token Storage**:
   - `token.json` is automatically created after first authentication
   - Store it securely
   - If compromised, delete it and re-authenticate

3. **Access Control**:
   - Limit OAuth 2.0 scopes to only what's needed
   - Regularly review and remove unused access
   - Keep the authorized user list minimal

## Troubleshooting

### Common Issues

1. **Authentication Failed**:
   - Verify `credentials.json` is present and valid
   - Check if token is expired (delete `token.json` and re-authenticate)
   - Ensure correct OAuth 2.0 scopes are enabled

2. **Calendar Operation Failed**:
   - Check internet connectivity
   - Verify calendar/event IDs exist
   - Ensure user has required permissions
   - Check for time zone issues in datetime strings

3. **Rate Limiting**:
   - Implement exponential backoff
   - Cache frequently accessed data
   - Batch operations when possible

### Debug Mode

```python
# Enable debug logging
handler = CalendarHandler(debug=True)
```

## API Reference

### CalendarHandler Class

```python
class CalendarHandler:
    def __init__(self, credentials_path="credentials.json", token_path="token.json", debug=False):
        """Initialize the calendar handler"""
        
    def authenticate(self):
        """Authenticate with Google Calendar API"""
        
    def get_calendars(self):
        """Get list of all calendars"""
        
    def add_event(self, title, start_time, duration_minutes, **kwargs):
        """Add new calendar event"""
        
    def update_event(self, event_id, **kwargs):
        """Update existing calendar event"""
        
    def delete_event(self, event_id):
        """Delete calendar event"""
        
    def get_events(self, start_time, end_time):
        """Get events in time range"""
        
    def check_availability(self, start_time, end_time):
        """Check if time slot is available"""
        
    def find_available_slots(self, date, duration_minutes, start_hour=9, end_hour=17):
        """Find available time slots"""
```

## Testing

```bash
# Run test suite
python test.py

# Run specific test
python -m unittest test.TestCalendarHandler.test_add_event
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Write tests for new features
4. Submit pull request

## Support

For issues and feature requests:
- Create GitHub issue
- Include detailed description
- Attach relevant logs
- Provide steps to reproduce 