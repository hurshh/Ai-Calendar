#!/usr/bin/env python3

from calendar_handler import CalendarHandler
from datetime import datetime, timedelta
import pytz
import re
from typing import Tuple, List, Dict, Optional

class CalendarChatbot:
    def __init__(self):
        """Initialize the chatbot with CalendarHandler"""
        self.handler = CalendarHandler()
        self.handler.authenticate()
        self.commands = {
            'schedule': self._handle_schedule,
            'show': self._handle_show,
            'find': self._handle_find,
            'update': self._handle_update,
            'delete': self._handle_delete,
            'help': self._handle_help
        }

    def _parse_datetime(self, date_str: str) -> str:
        """Convert various date formats to RFC3339 UTC format"""
        try:
            # Handle "tomorrow", "today", etc.
            if date_str.lower() == 'tomorrow':
                date = datetime.now() + timedelta(days=1)
            elif date_str.lower() == 'today':
                date = datetime.now()
            else:
                # Try to parse the provided date string
                date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
            
            # Convert to UTC
            utc_date = date.astimezone(pytz.UTC)
            return utc_date.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        except Exception as e:
            raise ValueError(f"Could not parse date: {date_str}. Please use format: YYYY-MM-DD HH:MM")

    def _parse_duration(self, duration_str: str) -> int:
        """Convert duration string to minutes"""
        try:
            # Extract number and unit
            match = re.match(r'(\d+)\s*(hour|hr|minute|min|m|h)s?', duration_str.lower())
            if not match:
                return 60  # default to 60 minutes
            
            number, unit = match.groups()
            number = int(number)
            
            if unit in ['hour', 'hr', 'h']:
                return number * 60
            else:
                return number
        except:
            return 60  # default to 60 minutes

    def _handle_schedule(self, query: str) -> str:
        """Handle scheduling new events"""
        try:
            # Extract title (everything between quotes)
            title_match = re.search(r'"([^"]*)"', query)
            if not title_match:
                return "Please provide event title in quotes. Example: schedule \"Team Meeting\" tomorrow at 10:00 for 1 hour"
            
            title = title_match.group(1)
            
            # Extract date and time
            date_match = re.search(r'(tomorrow|today|\d{4}-\d{2}-\d{2})\s*(?:at)?\s*(\d{1,2}:\d{2})', query)
            if not date_match:
                return "Please specify date and time. Example: tomorrow at 10:00"
            
            date_str = f"{date_match.group(1)} {date_match.group(2)}"
            start_time = self._parse_datetime(date_str)
            
            # Extract duration
            duration_match = re.search(r'for\s+(\d+\s*(?:hour|hr|minute|min|m|h)s?)', query)
            duration = self._parse_duration(duration_match.group(1) if duration_match else "1 hour")
            
            # Create event
            event_id = self.handler.add_event(
                title=title,
                start_time=start_time,
                duration_minutes=duration
            )
            
            if event_id:
                return f"✓ Scheduled: {title} for {duration} minutes"
            else:
                return "Failed to schedule event. Please try again."
            
        except ValueError as e:
            return str(e)
        except Exception as e:
            return f"Error scheduling event: {str(e)}"

    def _handle_show(self, query: str) -> str:
        """Handle showing calendar events"""
        try:
            # Default to showing today's events
            start_time = datetime.now(pytz.UTC)
            end_time = start_time + timedelta(days=1)
            
            if 'tomorrow' in query.lower():
                start_time = start_time + timedelta(days=1)
                end_time = start_time + timedelta(days=1)
            elif 'week' in query.lower():
                end_time = start_time + timedelta(days=7)
            
            events = self.handler.get_events(
                start_time=start_time.strftime('%Y-%m-%dT%H:%M:%S.000Z'),
                end_time=end_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')
            )
            
            if not events:
                return "No events found for the specified time period."
            
            response = []
            for event in events:
                start = event.get('start', {}).get('dateTime', 'Unknown')
                title = event.get('summary', 'Untitled Event')
                response.append(f"- {title} at {start}")
            
            return "\n".join(response)
            
        except Exception as e:
            return f"Error showing events: {str(e)}"

    def _handle_find(self, query: str) -> str:
        """Handle finding available time slots"""
        try:
            # Extract date
            date_match = re.search(r'(tomorrow|today|\d{4}-\d{2}-\d{2})', query)
            if not date_match:
                return "Please specify a date. Example: find slots tomorrow"
            
            date_str = date_match.group(1)
            if date_str == 'tomorrow':
                date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            elif date_str == 'today':
                date = datetime.now().strftime('%Y-%m-%d')
            else:
                date = date_str
            
            # Extract duration
            duration_match = re.search(r'(\d+\s*(?:hour|hr|minute|min|m|h)s?)', query)
            duration = self._parse_duration(duration_match.group(1) if duration_match else "1 hour")
            
            slots = self.handler.find_available_slots(
                date=date,
                duration_minutes=duration
            )
            
            if not slots:
                return "No available slots found for the specified time period."
            
            response = [f"Available {duration}-minute slots:"]
            for slot in slots[:5]:  # Show first 5 slots
                response.append(f"- {slot['start_time']} to {slot['end_time']}")
            
            if len(slots) > 5:
                response.append(f"... and {len(slots)-5} more slots available")
            
            return "\n".join(response)
            
        except Exception as e:
            return f"Error finding slots: {str(e)}"

    def _handle_update(self, query: str) -> str:
        """Handle updating events"""
        try:
            # Extract event ID (implement a way to reference events)
            event_id_match = re.search(r'event\s+(\w+)', query)
            if not event_id_match:
                return "Please specify event ID. Example: update event abc123 title \"New Title\""
            
            event_id = event_id_match.group(1)
            
            # Extract new title if provided
            title_match = re.search(r'title\s+"([^"]*)"', query)
            title = title_match.group(1) if title_match else None
            
            # Extract new time if provided
            time_match = re.search(r'time\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})', query)
            start_time = self._parse_datetime(time_match.group(1)) if time_match else None
            
            success = self.handler.update_event(
                event_id=event_id,
                title=title,
                start_time=start_time
            )
            
            if success:
                return "✓ Event updated successfully"
            else:
                return "Failed to update event. Please check the event ID and try again."
            
        except Exception as e:
            return f"Error updating event: {str(e)}"

    def _handle_delete(self, query: str) -> str:
        """Handle deleting events"""
        try:
            # Extract event ID
            event_id_match = re.search(r'event\s+(\w+)', query)
            if not event_id_match:
                return "Please specify event ID. Example: delete event abc123"
            
            event_id = event_id_match.group(1)
            
            success = self.handler.delete_event(event_id)
            
            if success:
                return "✓ Event deleted successfully"
            else:
                return "Failed to delete event. Please check the event ID and try again."
            
        except Exception as e:
            return f"Error deleting event: {str(e)}"

    def _handle_help(self, query: str) -> str:
        """Show help message"""
        return """Available commands:
1. Schedule an event:
   schedule "Event Title" tomorrow at 10:00 for 1 hour

2. Show events:
   show today
   show tomorrow
   show this week

3. Find available slots:
   find slots tomorrow
   find slots tomorrow for 30 minutes

4. Update event:
   update event <event_id> title "New Title"
   update event <event_id> time 2024-01-20 10:00

5. Delete event:
   delete event <event_id>

6. Help:
   help"""

    def process_query(self, query: str) -> str:
        """Process user query and return response"""
        query = query.strip().lower()
        
        # Check for command
        for cmd, handler in self.commands.items():
            if query.startswith(cmd):
                return handler(query)
        
        return "I didn't understand that command. Type 'help' to see available commands."

def main():
    """Main function to run the chatbot"""
    print("Calendar Chatbot")
    print("Type 'help' to see available commands")
    print("Type 'quit' to exit")
    print("=" * 50)
    
    chatbot = CalendarChatbot()
    
    while True:
        try:
            query = input("\nYou: ").strip()
            
            if query.lower() in ['quit', 'exit', 'bye']:
                print("Goodbye!")
                break
            
            response = chatbot.process_query(query)
            print(f"\nBot: {response}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nBot: An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 