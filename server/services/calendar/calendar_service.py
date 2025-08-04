"""
Calendar service handling calendar operations
"""

from services.calendar.calendar_handler import CalendarHandler

class CalendarService:
    def __init__(self):
        """Initialize calendar service"""
        self.handler = CalendarHandler()
        try:
            self.handler.authenticate()
        except Exception as e:
            print(f"Error authenticating calendar: {e}")
            self.handler = None

    def is_available(self) -> bool:
        """Check if calendar service is available"""
        return self.handler is not None

    def get_events(self, start_time: str, end_time: str):
        """Get calendar events"""
        return self.handler.get_events(start_time=start_time, end_time=end_time)

    def add_event(self, title: str, start_time: str, duration_minutes: int, description: str = ""):
        """Add a new calendar event"""
        return self.handler.add_event(
            title=title,
            start_time=start_time,
            duration_minutes=duration_minutes,
            description=description
        )

    def delete_event(self, event_id: str) -> bool:
        """Delete a calendar event"""
        return self.handler.delete_event(event_id)

    def update_event(self, event_id: str, **updates) -> bool:
        """Update a calendar event"""
        return self.handler.update_event(event_id, **updates) 