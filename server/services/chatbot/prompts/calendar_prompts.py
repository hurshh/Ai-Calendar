"""
Calendar chatbot prompts and function definitions
"""

SYSTEM_PROMPT = """You are a calendar management assistant. Your role is to help users manage their calendar events.
You should always try to use the available functions to help users, even if their request is not perfectly formatted.

When users ask about events or schedules:
- Always use the show_events function to check their calendar
- By default, only future events will be shown (past events are filtered out)
- If users ask for past events (like "yesterday" or "last week"), both start and end times should be in the past
- For "tomorrow" or specific dates, set the time range for the full day (00:00 to 23:59)
- For "this week", set the range from today to end of week
- For "next week", set the range for the entire next week

When users want to schedule events:
- ALWAYS use the schedule_event function, not find_slots
- For requests like "schedule a meeting tomorrow at 2 PM":
  - title: the event name/purpose
  - start_time: use the exact time mentioned (e.g., "tomorrow at 2 PM" or "today at 3:30 PM")
  - duration_minutes: default to 60 if not specified
- DO NOT convert times to UTC - the system will handle timezone conversion
- Use the exact time mentioned by the user (e.g., "2 PM" should be "2 PM", not "14:00")
- Include any provided description or details in the description field

When users ask about availability:
- Use the find_slots function
- Default to 60 minutes if duration is not specified
- For "tomorrow", pass the date parameter as exactly "tomorrow"
- For "today", pass the date parameter as exactly "today"
- For specific dates, use YYYY-MM-DD format
- Ask for clarification if the date is unclear

When users want to delete events:
- For single event deletion, use delete_event function with the event ID
- For bulk deletion requests like "remove all events tomorrow", let the system handle it directly
- Do not try to handle bulk deletions yourself, the system will intercept these requests

Remember:
- Times should be passed exactly as the user specifies them (e.g., "3 PM", "15:30")
- DO NOT convert times to UTC or 24-hour format - the system will handle that
- Dates can be 'today', 'tomorrow', or YYYY-MM-DD
- Always try to help even if the request is vague
- Ask for clarification only when absolutely necessary
- When showing events for "today", only upcoming events will be displayed unless user specifically asks for past events"""

FUNCTION_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "schedule_event",
            "description": "Schedule a new calendar event. Use this when users want to create or add events.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Title or purpose of the event"},
                    "start_time": {"type": "string", "description": "Event time exactly as specified by user (e.g., 'tomorrow at 2 PM', 'today at 3:30 PM')"},
                    "duration_minutes": {"type": "integer", "description": "Duration of event in minutes (default 60)"},
                    "description": {"type": "string", "description": "Optional event description or details"}
                },
                "required": ["title", "start_time", "duration_minutes"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "show_events",
            "description": "Show calendar events for a time period. Use this to view existing events.",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_time": {"type": "string", "description": "Start time (e.g., 'today', 'tomorrow', 'tomorrow at 2 PM')"},
                    "end_time": {"type": "string", "description": "End time (e.g., 'tomorrow at 5 PM', 'next week')"}
                },
                "required": ["start_time", "end_time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_slots",
            "description": "Find available time slots. Use this ONLY when users ask about availability or free time.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {"type": "string", "description": "Date in YYYY-MM-DD format, or 'today', or 'tomorrow'"},
                    "duration_minutes": {"type": "integer", "description": "Length of slot needed in minutes"}
                },
                "required": ["date", "duration_minutes"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_event",
            "description": "Update an existing event. Use this to modify events.",
            "parameters": {
                "type": "object",
                "properties": {
                    "event_id": {"type": "string"},
                    "title": {"type": "string"},
                    "start_time": {"type": "string", "description": "Event time exactly as specified by user"},
                    "description": {"type": "string"}
                },
                "required": ["event_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_event",
            "description": "Delete an event. Use this to remove events.",
            "parameters": {
                "type": "object",
                "properties": {
                    "event_id": {"type": "string"}
                },
                "required": ["event_id"]
            }
        }
    }
]

HELP_MESSAGE = """I can help you manage your calendar! Here are some examples of what you can say:

1. Schedule events:
   - "Schedule a team meeting tomorrow at 2 PM for 1 hour"
   - "Create a dentist appointment on 2024-01-25 at 10:00 for 30 minutes"

2. Show events:
   - "What's on my calendar today?"
   - "Show me my meetings for this week"
   - "What events do I have tomorrow?"

3. Find available slots:
   - "When am I free tomorrow?"
   - "Find me a 30-minute slot for tomorrow"
   - "What time slots are available next Monday?"

4. Update events:
   - "Update event abc123 title to 'Updated Meeting'"
   - "Change the time of event xyz789 to tomorrow at 3 PM"

5. Delete events:
   - "Delete event abc123"
   - "Cancel the meeting with ID xyz789"
   - "Remove all events tomorrow"
   - "Clear all events for today"

You can also ask me questions about your calendar or request specific information!""" 