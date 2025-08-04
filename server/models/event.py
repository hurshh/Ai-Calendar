"""
Calendar Event Model
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Event:
    """Calendar event data model"""
    id: str
    title: str
    start_time: datetime
    end_time: datetime
    description: Optional[str] = None
    location: Optional[str] = None
    
    @classmethod
    def from_google_event(cls, google_event: dict) -> 'Event':
        """Create Event from Google Calendar event"""
        return cls(
            id=google_event.get('id', ''),
            title=google_event.get('summary', 'Untitled Event'),
            start_time=datetime.fromisoformat(google_event['start']['dateTime'].replace('Z', '+00:00')),
            end_time=datetime.fromisoformat(google_event['end']['dateTime'].replace('Z', '+00:00')),
            description=google_event.get('description'),
            location=google_event.get('location')
        )
    
    def to_dict(self) -> dict:
        """Convert event to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'start': self.start_time.isoformat(),
            'end': self.end_time.isoformat(),
            'description': self.description,
            'location': self.location
        }
    
    def format_time(self, dt: datetime, timezone=None) -> str:
        """Format datetime for display"""
        if timezone:
            dt = dt.astimezone(timezone)
        return dt.strftime("%B %d, %Y at %I:%M %p") 