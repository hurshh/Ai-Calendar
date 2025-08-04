"""
Calendar controller handling calendar operations
"""

from flask import jsonify
from datetime import datetime, timedelta
import pytz
from services.calendar.calendar_service import CalendarService
from utils.time.time_utils import format_events_for_display

class CalendarController:
    def __init__(self):
        """Initialize calendar controller"""
        self.service = CalendarService()

    def get_events(self):
        """Get calendar events for display"""
        try:
            if not self.service.is_available():
                return jsonify({'error': 'Calendar not available'}), 500
            
            # Get events for the next 7 days by default
            start_date = datetime.now(pytz.UTC)
            end_date = start_date + timedelta(days=7)
            
            start_time = start_date.strftime('%Y-%m-%dT%H:%M:%S.000Z')
            end_time = end_date.strftime('%Y-%m-%dT%H:%M:%S.000Z')
            
            events = self.service.get_events(start_time=start_time, end_time=end_time)
            formatted_events = format_events_for_display(events)
            
            return jsonify({'events': formatted_events})
            
        except Exception as e:
            print(f"Error getting events: {e}")
            return jsonify({'error': str(e)}), 500 