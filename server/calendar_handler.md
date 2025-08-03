# Calendar Handler Documentation

## Overview

The `CalendarHandler` class provides a comprehensive interface for Google Calendar operations including:
- OAuth 2.0 authentication
- Event management (create, read, update, delete)
- Calendar operations
- Availability checking
- Free/busy information

## Class Methods

### 1. Authentication

#### `__init__(credentials_file: str = 'credentials.json', token_file: str = 'token.json')`
Initialize the Calendar Handler with optional custom file paths.
```python
handler = CalendarHandler(
    credentials_file='path/to/credentials.json',
    token_file='path/to/token.json'
)
```

#### `authenticate() -> bool`
Authenticate with Google Calendar API using OAuth 2.0.
```python
if handler.authenticate():
    print("Authentication successful")
```

### 2. Calendar Management

#### `get_calendars() -> List[Dict]`
Get all accessible calendars.
```python
calendars = handler.get_calendars()
for calendar in calendars:
    print(f"Calendar: {calendar['summary']} (ID: {calendar['id']})")
```

#### `set_default_calendar(calendar_id: str) -> bool`
Set the default calendar for operations.
```python
success = handler.set_default_calendar("primary")
```

### 3. Event Management

#### `add_event()`
```python
def add_event(
    title: str,
    start_time: str,
    duration_minutes: int = 60,
    description: str = "",
    location: str = "",
    attendees: List[str] = None,
    calendar_id: str = None,
    all_day: bool = False,
    reminders: Dict = None
) -> Optional[str]
```
Creates a new event in the calendar.

Example:
```python
event_id = handler.add_event(
    title="Team Meeting",
    start_time="2024-01-20T10:00:00.000Z",
    duration_minutes=60,
    description="Weekly team sync",
    location="Conference Room A",
    attendees=["team@company.com"]
)
```

#### `delete_event()`
```python
def delete_event(
    event_id: str,
    calendar_id: str = None
) -> bool
```
Delete an event from the calendar.

Example:
```python
success = handler.delete_event("event_id_here")
```

#### `update_event()`
```python
def update_event(
    event_id: str,
    title: str = None,
    start_time: str = None,
    end_time: str = None,
    description: str = None,
    location: str = None,
    attendees: List[str] = None,
    calendar_id: str = None
) -> bool
```
Update an existing event.

Example:
```python
success = handler.update_event(
    event_id="event_id_here",
    title="Updated Meeting",
    description="Updated description"
)
```

#### `get_event()`
```python
def get_event(
    event_id: str,
    calendar_id: str = None
) -> Optional[Dict]
```
Get a specific event by ID.

Example:
```python
event = handler.get_event("event_id_here")
if event:
    print(f"Event: {event['summary']}")
```

#### `get_events()`
```python
def get_events(
    start_time: str = None,
    end_time: str = None,
    calendar_id: str = None,
    max_results: int = 50
) -> List[Dict]
```
Get events from a calendar within a time range.

Example:
```python
events = handler.get_events(
    start_time="2024-01-20T00:00:00.000Z",
    end_time="2024-01-21T00:00:00.000Z"
)
```

### 4. Availability Checking

#### `check_availability()`
```python
def check_availability(
    start_time: str,
    end_time: str,
    calendar_id: str = None
) -> Tuple[bool, List[Dict]]
```
Check if a time slot is available (no conflicts).

Example:
```python
is_available, conflicts = handler.check_availability(
    start_time="2024-01-20T10:00:00.000Z",
    end_time="2024-01-20T11:00:00.000Z"
)
```

#### `find_available_slots()`
```python
def find_available_slots(
    date: str,
    duration_minutes: int = 60,
    start_hour: int = 9,
    end_hour: int = 17,
    calendar_id: str = None
) -> List[Dict]
```
Find available time slots on a specific date.

Example:
```python
slots = handler.find_available_slots(
    date="2024-01-20",
    duration_minutes=60,
    start_hour=9,
    end_hour=17
)
```

#### `get_free_busy()`
```python
def get_free_busy(
    start_time: str,
    end_time: str,
    calendar_ids: List[str] = None
) -> Dict
```
Get free/busy information for specified calendars.

Example:
```python
free_busy = handler.get_free_busy(
    start_time="2024-01-20T00:00:00.000Z",
    end_time="2024-01-21T00:00:00.000Z",
    calendar_ids=["primary", "work@company.com"]
)
```

## Important Notes

### Time Format
All time parameters should be in RFC3339 format with UTC timezone:
- Format: `YYYY-MM-DDThh:mm:ss.000Z`
- Example: `2024-01-20T10:00:00.000Z`

### Calendar IDs
- Use `"primary"` for the user's primary calendar
- For other calendars, use the calendar ID from `get_calendars()`
- If `calendar_id` is not specified, the default calendar is used

### Reminders
Default reminders for new events:
- Email: 24 hours before
- Popup: 10 minutes before

Custom reminders format:
```python
reminders = {
    'useDefault': False,
    'overrides': [
        {'method': 'email', 'minutes': 60},  # 1 hour before
        {'method': 'popup', 'minutes': 15}   # 15 minutes before
    ]
}
```

### Error Handling
All methods include comprehensive error handling:
- Authentication errors are logged with setup instructions
- API errors are caught and logged with details
- Invalid parameters are validated and reported
- Network issues are handled gracefully

## Example Usage

### Basic Calendar Operations
```python
# Initialize and authenticate
handler = CalendarHandler()
handler.authenticate()

# Get calendars
calendars = handler.get_calendars()
print(f"Found {len(calendars)} calendars")

# Create event
event_id = handler.add_event(
    title="Team Meeting",
    start_time="2024-01-20T10:00:00.000Z",
    duration_minutes=60
)

# Check availability
is_available, conflicts = handler.check_availability(
    start_time="2024-01-20T10:00:00.000Z",
    end_time="2024-01-20T11:00:00.000Z"
)

# Find available slots
available_slots = handler.find_available_slots(
    date="2024-01-20",
    duration_minutes=60
)

# Delete event
handler.delete_event(event_id)
```

### Advanced Usage
```python
# Create event with attendees and reminders
event_id = handler.add_event(
    title="Project Review",
    start_time="2024-01-20T14:00:00.000Z",
    duration_minutes=90,
    description="Quarterly project review meeting",
    location="Conference Room B",
    attendees=["team@company.com", "manager@company.com"],
    reminders={
        'useDefault': False,
        'overrides': [
            {'method': 'email', 'minutes': 24 * 60},  # 1 day before
            {'method': 'popup', 'minutes': 30}        # 30 minutes before
        ]
    }
)

# Update event
handler.update_event(
    event_id=event_id,
    description="Updated: Quarterly project review with stakeholders",
    attendees=["team@company.com", "manager@company.com", "stakeholder@company.com"]
)

# Get free/busy information
free_busy = handler.get_free_busy(
    start_time="2024-01-20T00:00:00.000Z",
    end_time="2024-01-21T00:00:00.000Z",
    calendar_ids=["primary", "team@company.com"]
)
```

## Best Practices

1. **Authentication**
   - Store credentials securely
   - Handle token refresh automatically
   - Use environment variables for sensitive data

2. **Event Management**
   - Always use UTC timestamps
   - Include timezone information
   - Set appropriate reminders
   - Handle recurring events carefully

3. **Availability Checking**
   - Consider buffer time between meetings
   - Check multiple calendars when necessary
   - Handle all-day events appropriately

4. **Error Handling**
   - Implement proper error recovery
   - Log important operations
   - Validate input parameters
   - Handle rate limiting

## Troubleshooting

Common issues and solutions:

1. **Authentication Failed**
   - Verify credentials.json exists
   - Check token expiration
   - Ensure correct OAuth scopes

2. **Event Creation Failed**
   - Validate timestamp format
   - Check calendar permissions
   - Verify attendee email addresses

3. **Availability Issues**
   - Confirm timezone handling
   - Check for recurring events
   - Verify calendar visibility

4. **Performance**
   - Use appropriate time ranges
   - Implement caching if needed
   - Batch operations when possible 