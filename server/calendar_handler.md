# CalendarHandler Documentation

A comprehensive Google Calendar management handler that provides authentication, event management, availability checking, and calendar operations.

## Overview

The `CalendarHandler` class offers a complete interface for managing Google Calendar operations including:
- OAuth 2.0 authentication
- Event creation, deletion, and updates
- Availability checking and conflict detection
- Calendar management and multi-calendar support
- Free/busy information retrieval

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up Google Cloud Console credentials:
   - Go to https://console.cloud.google.com/
   - Create a project or select existing one
   - Enable Google Calendar API
   - Create OAuth 2.0 credentials (Desktop application)
   - Download `credentials.json` and place it in the project directory

## Basic Usage

```python
from calendar_handler import CalendarHandler

# Initialize handler
handler = CalendarHandler()

# Authenticate
if handler.authenticate():
    # Use calendar operations
    calendars = handler.get_calendars()
    print(f"Found {len(calendars)} calendars")
```

## Class Methods

### Authentication

#### `authenticate() -> bool`
Authenticates with Google Calendar API using OAuth 2.0.

**Returns:**
- `bool`: True if authentication successful, False otherwise

**Example:**
```python
if handler.authenticate():
    print("Authentication successful")
else:
    print("Authentication failed")
```

### Calendar Management

#### `get_calendars() -> List[Dict]`
Retrieves all accessible calendars.

**Returns:**
- `List[Dict]`: List of calendar dictionaries with id, summary, description, timeZone, primary, selected, accessRole

**Example:**
```python
calendars = handler.get_calendars()
for calendar in calendars:
    print(f"Calendar: {calendar['summary']} (ID: {calendar['id']})")
```

#### `set_default_calendar(calendar_id: str) -> bool`
Sets the default calendar for operations.

**Parameters:**
- `calendar_id` (str): Calendar ID to set as default

**Returns:**
- `bool`: True if successful, False otherwise

**Example:**
```python
success = handler.set_default_calendar("primary")
if success:
    print("Default calendar set successfully")
```

### Event Management

#### `add_event(title: str, start_time: str, duration_minutes: int = 60, description: str = "", location: str = "", attendees: List[str] = None, calendar_id: str = None, all_day: bool = False, reminders: Dict = None) -> Optional[str]`
Creates a new event in the calendar.

**Parameters:**
- `title` (str): Event title
- `start_time` (str): Start time in ISO format (e.g., "2024-01-15T10:00:00")
- `duration_minutes` (int): Event duration in minutes (default: 60)
- `description` (str): Event description (default: "")
- `location` (str): Event location (default: "")
- `attendees` (List[str]): List of attendee email addresses (default: None)
- `calendar_id` (str): Calendar ID (uses default if None)
- `all_day` (bool): Whether this is an all-day event (default: False)
- `reminders` (Dict): Custom reminders configuration (default: None)

**Returns:**
- `str`: Event ID if successful, None otherwise

**Example:**
```python
event_id = handler.add_event(
    title="Team Meeting",
    start_time="2024-01-20T14:00:00",
    duration_minutes=90,
    description="Weekly team sync",
    location="Conference Room A",
    attendees=["team@company.com", "manager@company.com"]
)
```

#### `delete_event(event_id: str, calendar_id: str = None) -> bool`
Deletes an event from the calendar.

**Parameters:**
- `event_id` (str): ID of the event to delete
- `calendar_id` (str): Calendar ID (uses default if None)

**Returns:**
- `bool`: True if successful, False otherwise

**Example:**
```python
success = handler.delete_event("event_id_here")
if success:
    print("Event deleted successfully")
```

#### `update_event(event_id: str, title: str = None, start_time: str = None, end_time: str = None, description: str = None, location: str = None, attendees: List[str] = None, calendar_id: str = None) -> bool`
Updates an existing event.

**Parameters:**
- `event_id` (str): ID of the event to update
- `title` (str): New event title (optional)
- `start_time` (str): New start time (optional)
- `end_time` (str): New end time (optional)
- `description` (str): New description (optional)
- `location` (str): New location (optional)
- `attendees` (List[str]): New list of attendees (optional)
- `calendar_id` (str): Calendar ID (uses default if None)

**Returns:**
- `bool`: True if successful, False otherwise

**Example:**
```python
success = handler.update_event(
    event_id="event_id_here",
    title="Updated Meeting Title",
    description="Updated meeting description"
)
```

#### `get_event(event_id: str, calendar_id: str = None) -> Optional[Dict]`
Retrieves a specific event by ID.

**Parameters:**
- `event_id` (str): ID of the event to retrieve
- `calendar_id` (str): Calendar ID (uses default if None)

**Returns:**
- `Dict`: Event data if found, None otherwise

**Example:**
```python
event = handler.get_event("event_id_here")
if event:
    print(f"Event: {event.get('summary')}")
    print(f"Start: {event.get('start')}")
```

#### `get_events(start_time: str = None, end_time: str = None, calendar_id: str = None, max_results: int = 50) -> List[Dict]`
Retrieves events from a calendar within a time range.

**Parameters:**
- `start_time` (str): Start time in ISO format (defaults to now)
- `end_time` (str): End time in ISO format (defaults to 7 days from now)
- `calendar_id` (str): Calendar ID (uses default if None)
- `max_results` (int): Maximum number of events to return (default: 50)

**Returns:**
- `List[Dict]`: List of event dictionaries

**Example:**
```python
events = handler.get_events(
    start_time="2024-01-20T00:00:00",
    end_time="2024-01-21T23:59:59",
    max_results=20
)
for event in events:
    print(f"Event: {event.get('summary')}")
```

### Availability Checking

#### `check_availability(start_time: str, end_time: str, calendar_id: str = None) -> Tuple[bool, List[Dict]]`
Checks if a time slot is available (no conflicts).

**Parameters:**
- `start_time` (str): Start time in ISO format
- `end_time` (str): End time in ISO format
- `calendar_id` (str): Calendar ID (uses default if None)

**Returns:**
- `Tuple[bool, List[Dict]]`: (is_available, conflicting_events)

**Example:**
```python
is_available, conflicts = handler.check_availability(
    start_time="2024-01-20T14:00:00",
    end_time="2024-01-20T15:30:00"
)

if is_available:
    print("Time slot is available")
else:
    print(f"Found {len(conflicts)} conflicts")
```

#### `find_available_slots(date: str, duration_minutes: int = 60, start_hour: int = 9, end_hour: int = 17, calendar_id: str = None) -> List[Dict]`
Finds available time slots on a specific date.

**Parameters:**
- `date` (str): Date in YYYY-MM-DD format
- `duration_minutes` (int): Duration of desired slot in minutes (default: 60)
- `start_hour` (int): Start hour (24-hour format, default: 9)
- `end_hour` (int): End hour (24-hour format, default: 17)
- `calendar_id` (str): Calendar ID (uses default if None)

**Returns:**
- `List[Dict]`: List of available time slots with start_time, end_time, duration_minutes

**Example:**
```python
slots = handler.find_available_slots(
    date="2024-01-20",
    duration_minutes=60,
    start_hour=9,
    end_hour=17
)

for slot in slots:
    print(f"Available: {slot['start_time']} to {slot['end_time']}")
```

#### `get_free_busy(start_time: str, end_time: str, calendar_ids: List[str] = None) -> Dict`
Gets free/busy information for specified calendars.

**Parameters:**
- `start_time` (str): Start time in ISO format
- `end_time` (str): End time in ISO format
- `calendar_ids` (List[str]): List of calendar IDs (uses default if None)

**Returns:**
- `Dict`: Free/busy information

**Example:**
```python
free_busy = handler.get_free_busy(
    start_time="2024-01-20T00:00:00",
    end_time="2024-01-21T23:59:59",
    calendar_ids=["primary", "work@company.com"]
)
```

## Configuration

### Default Settings

The handler uses these default settings:
- **Default Calendar**: 'primary'
- **Timezone**: 'UTC'
- **Credentials File**: 'credentials.json'
- **Token File**: 'token.json'

### Custom Configuration

You can customize the handler during initialization:

```python
handler = CalendarHandler(
    credentials_file='path/to/credentials.json',
    token_file='path/to/token.json'
)
```

## Error Handling

All methods include comprehensive error handling:
- Authentication errors are logged with setup instructions
- API errors are caught and logged with details
- Invalid parameters are validated and reported
- Network issues are handled gracefully

## Time Format

All time parameters should be in ISO 8601 format:
- **Date and Time**: "2024-01-20T14:00:00"
- **Date Only**: "2024-01-20" (for all-day events)
- **With Timezone**: "2024-01-20T14:00:00+05:30"

## Reminders

Default reminders are automatically added to new events:
- Email reminder: 24 hours before
- Popup reminder: 10 minutes before

Custom reminders can be specified:

```python
custom_reminders = {
    'useDefault': False,
    'overrides': [
        {'method': 'email', 'minutes': 60},   # 1 hour before
        {'method': 'popup', 'minutes': 15}    # 15 minutes before
    ]
}

event_id = handler.add_event(
    title="Meeting",
    start_time="2024-01-20T14:00:00",
    reminders=custom_reminders
)
```

## Complete Example

```python
from calendar_handler import CalendarHandler
from datetime import datetime, timedelta

# Initialize and authenticate
handler = CalendarHandler()
if not handler.authenticate():
    exit(1)

# Get calendars
calendars = handler.get_calendars()
print(f"Access to {len(calendars)} calendars")

# Check availability for tomorrow
tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
start_time = f"{tomorrow}T10:00:00"
end_time = f"{tomorrow}T11:00:00"

is_available, conflicts = handler.check_availability(start_time, end_time)

if is_available:
    # Create event
    event_id = handler.add_event(
        title="Team Meeting",
        start_time=start_time,
        duration_minutes=60,
        description="Weekly team sync",
        attendees=["team@company.com"]
    )
    
    if event_id:
        print(f"Event created: {event_id}")
        
        # Update event
        handler.update_event(event_id, description="Updated description")
        
        # Delete event
        handler.delete_event(event_id)
        print("Event deleted")
else:
    print("Time slot not available")
```

## Dependencies

Required Python packages:
- google-auth==2.23.4
- google-auth-oauthlib==1.1.0
- google-auth-httplib2==0.1.1
- google-api-python-client==2.108.0
- pytz==2023.3

## License

This calendar handler is provided as-is for educational and development purposes. 