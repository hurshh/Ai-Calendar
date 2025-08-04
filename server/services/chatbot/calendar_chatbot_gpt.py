"""
GPT-powered calendar chatbot service
"""

from services.calendar_handler import CalendarHandler
from datetime import datetime, timedelta
import pytz
import re
import os
from typing import Tuple, List, Dict, Optional
from openai import OpenAI
from config.settings import OPENAI_MODEL

class CalendarGPTBot:
    def __init__(self, api_key: str):
        """Initialize the chatbot with CalendarHandler and GPT"""
        self.handler = CalendarHandler()
        self.handler.authenticate()
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.openai.com/v1"  # Explicitly set the base URL
        )
        
        # Get local timezone
        self.local_timezone = datetime.now().astimezone().tzinfo
        
        # System prompt to define chatbot's behavior
        self.system_prompt = """You are a calendar management assistant. Your role is to help users manage their calendar events.
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

    def _get_gpt_response(self, user_message: str) -> dict:
        """Get structured response from GPT"""
        try:
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            tools = [
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
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )
            
            # Get the first choice's message
            message = response.choices[0].message
            
            # Debug print
            print(f"DEBUG - GPT Response: {message}")
            
            return message
            
        except Exception as e:
            print(f"Error getting GPT response: {str(e)}")
            return None

    def _parse_datetime(self, date_str: str) -> str:
        """Convert various date formats to RFC3339 UTC format"""
        try:
            # Handle "tomorrow", "today", etc. with time
            if 'tomorrow' in date_str.lower():
                base_date = datetime.now(self.local_timezone) + timedelta(days=1)
                # Check if time is specified (e.g., "tomorrow at 2pm")
                if 'at' in date_str.lower():
                    time_part = date_str.lower().split('at')[1].strip()
                    # Convert 12-hour format to 24-hour
                    if 'pm' in time_part:
                        hour = int(time_part.replace('pm', '').strip())
                        hour = hour if hour == 12 else hour + 12
                        base_date = base_date.replace(hour=hour, minute=0)
                    elif 'am' in time_part:
                        hour = int(time_part.replace('am', '').strip())
                        hour = 0 if hour == 12 else hour
                        base_date = base_date.replace(hour=hour, minute=0)
                    else:
                        # Assume 24-hour format
                        hour = int(time_part.strip())
                        base_date = base_date.replace(hour=hour, minute=0)
                else:
                    # If no time specified, use current time
                    base_date = base_date.replace(hour=datetime.now(self.local_timezone).hour, 
                                               minute=datetime.now(self.local_timezone).minute)
            elif 'today' in date_str.lower():
                base_date = datetime.now(self.local_timezone)
                # Similar time parsing as above
                if 'at' in date_str.lower():
                    time_part = date_str.lower().split('at')[1].strip()
                    if 'pm' in time_part:
                        hour = int(time_part.replace('pm', '').strip())
                        hour = hour if hour == 12 else hour + 12
                        base_date = base_date.replace(hour=hour, minute=0)
                    elif 'am' in time_part:
                        hour = int(time_part.replace('am', '').strip())
                        hour = 0 if hour == 12 else hour
                        base_date = base_date.replace(hour=hour, minute=0)
                    else:
                        hour = int(time_part.strip())
                        base_date = base_date.replace(hour=hour, minute=0)
            else:
                # Try to parse the provided date string
                try:
                    # First try parsing as local time
                    base_date = datetime.fromisoformat(date_str)
                    if base_date.tzinfo is None:
                        # If no timezone was specified, assume local time
                        base_date = base_date.replace(tzinfo=self.local_timezone)
                except ValueError:
                    # If that fails, try parsing as UTC
                    base_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            
            # Convert to UTC
            utc_date = base_date.astimezone(pytz.UTC)
            return utc_date.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        except Exception as e:
            print(f"Date parsing error: {e}")
            raise ValueError(f"Could not parse date: {date_str}. Please use a clear date/time format.")

    def _format_event_time(self, time_str: str) -> str:
        """Format event time for display"""
        try:
            dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
            local_dt = dt.astimezone(self.local_timezone)  # Convert to local time
            return local_dt.strftime("%B %d, %Y at %I:%M %p")
        except:
            return time_str

    def handle_schedule_event(self, params: dict) -> str:
        """Handle scheduling new events"""
        try:
            event_id = self.handler.add_event(
                title=params['title'],
                start_time=self._parse_datetime(params['start_time']),
                duration_minutes=params['duration_minutes'],
                description=params.get('description', '')
            )
            
            if event_id:
                return f"✓ Successfully scheduled: {params['title']}\n" \
                       f"Start: {self._format_event_time(params['start_time'])}\n" \
                       f"Duration: {params['duration_minutes']} minutes\n" \
                       f"Event ID: {event_id}"
            else:
                return "Failed to schedule event. Please try again."
            
        except Exception as e:
            print(f"Error scheduling event: {e}")  # Log the error
            return f"Error scheduling event: {str(e)}"

    def handle_show_events(self, params: dict) -> str:
        """Handle showing calendar events"""
        try:
            # Convert times to proper format
            start_time = self._parse_datetime(params['start_time'])
            end_time = self._parse_datetime(params['end_time'])
            
            # Get current time for comparison
            current_time = datetime.now(pytz.UTC).strftime('%Y-%m-%dT%H:%M:%S.000Z')
            current_dt = datetime.fromisoformat(current_time.replace('Z', '+00:00'))
            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            
            # Only show future events unless both start and end are in the past
            # (which indicates user explicitly wants to see past events)
            if start_dt < current_dt and end_dt > current_dt:
                # If start is in past but end is in future (e.g., "today"), 
                # adjust start to current time to show only future events
                start_time = current_time
                adjusted_message = " (showing only upcoming events)"
            elif start_dt < current_dt and end_dt <= current_dt:
                # Both start and end are in past - user wants past events, keep as-is
                adjusted_message = ""
            else:
                # Start is in future or current - keep as-is
                adjusted_message = ""
            
            events = self.handler.get_events(
                start_time=start_time,
                end_time=end_time
            )
            
            if not events:
                return f"No events found between {self._format_event_time(start_time)} and {self._format_event_time(end_time)}."
            
            response = [f"Here are your events between {self._format_event_time(start_time)} and {self._format_event_time(end_time)}{adjusted_message}:"]
            for event in events:
                start = event.get('start', {}).get('dateTime', 'Unknown')
                title = event.get('summary', 'Untitled Event')
                description = event.get('description', '')
                location = event.get('location', '')
                
                event_str = f"- {title} at {self._format_event_time(start)}"
                if location:
                    event_str += f" ({location})"
                if description:
                    event_str += f"\n  Description: {description}"
                
                response.append(event_str)
            
            return "\n".join(response)
            
        except Exception as e:
            print(f"Error showing events: {str(e)}")
            return "Sorry, I had trouble retrieving your events. Please try again."

    def handle_find_slots(self, params: dict) -> str:
        """Handle finding available time slots"""
        try:
            # Convert date string to proper format
            if params['date'].lower() == 'tomorrow':
                date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            elif params['date'].lower() == 'today':
                date = datetime.now().strftime('%Y-%m-%d')
            else:
                date = params['date']

            # Create time range for the entire day
            start_of_day = f"{date}T00:00:00.000Z"
            end_of_day = f"{date}T23:59:59.999Z"
            
            # Get all events for the day
            events = self.handler.get_events(
                start_time=start_of_day,
                end_time=end_of_day
            )
            
            # Find available slots
            slots = []
            current_time = datetime.strptime(f"{date}T09:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
            end_time = datetime.strptime(f"{date}T17:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
            duration = timedelta(minutes=params['duration_minutes'])
            
            while current_time + duration <= end_time:
                slot_end = current_time + duration
                
                # Check if slot conflicts with any event
                is_available = True
                for event in events:
                    event_start = datetime.fromisoformat(event['start']['dateTime'].replace('Z', '+00:00'))
                    event_end = datetime.fromisoformat(event['end']['dateTime'].replace('Z', '+00:00'))
                    
                    if (event_start < slot_end and event_end > current_time):
                        is_available = False
                        break
                
                if is_available:
                    slots.append({
                        'start_time': current_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'end_time': slot_end.strftime("%Y-%m-%dT%H:%M:%S.000Z")
                    })
                
                # Move to next 30-minute slot
                current_time += timedelta(minutes=30)
            
            if not slots:
                return f"No available {params['duration_minutes']}-minute slots found for {date}."
            
            response = [f"Available {params['duration_minutes']}-minute slots for {date}:"]
            for slot in slots[:5]:
                start = self._format_event_time(slot['start_time'])
                end = self._format_event_time(slot['end_time'])
                response.append(f"- {start} to {end}")
            
            if len(slots) > 5:
                response.append(f"... and {len(slots)-5} more slots available")
            
            return "\n".join(response)
            
        except Exception as e:
            print(f"Error finding slots: {str(e)}")
            return "Sorry, I had trouble finding available slots. Please try again."

    def handle_update_event(self, params: dict) -> str:
        """Handle updating events"""
        try:
            updates = {}
            if 'title' in params:
                updates['title'] = params['title']
            if 'start_time' in params:
                updates['start_time'] = self._parse_datetime(params['start_time'])
            if 'description' in params:
                updates['description'] = params['description']
            
            success = self.handler.update_event(
                event_id=params['event_id'],
                **updates
            )
            
            if success:
                return "✓ Event updated successfully"
            else:
                return "Failed to update event. Please check the event ID and try again."
            
        except Exception as e:
            return f"Error updating event: {str(e)}"

    def handle_delete_event(self, params: dict) -> str:
        """Handle deleting events"""
        try:
            success = self.handler.delete_event(params['event_id'])
            
            if success:
                return "✓ Event deleted successfully"
            else:
                return "Failed to delete event. Please check the event ID and try again."
            
        except Exception as e:
            return f"Error deleting event: {str(e)}"

    def handle_bulk_delete(self, start_time: str, end_time: str) -> str:
        """Handle deleting multiple events in a time range"""
        try:
            # First get all events in the range
            events = self.handler.get_events(
                start_time=self._parse_datetime(start_time),
                end_time=self._parse_datetime(end_time)
            )
            
            if not events:
                return "No events found in the specified time period."
            
            # Delete each event
            deleted_count = 0
            for event in events:
                event_id = event.get('id')
                if event_id and self.handler.delete_event(event_id):
                    deleted_count += 1
            
            if deleted_count > 0:
                return f"✓ Successfully deleted {deleted_count} event{'s' if deleted_count > 1 else ''}"
            else:
                return "Failed to delete events. Please try again."
            
        except Exception as e:
            print(f"Error in bulk delete: {e}")
            return f"Error deleting events: {str(e)}"

    def process_query(self, query: str) -> str:
        """Process user query using GPT and execute calendar operations"""
        # Handle bulk delete requests directly without GPT
        query_lower = query.lower()
        if any(phrase in query_lower for phrase in [
            "remove all events",
            "delete all events",
            "clear all events",
            "cancel all events"
        ]):
            # Extract time period
            if "tomorrow" in query_lower:
                tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
                start_time = f"{tomorrow}T00:00:00Z"
                end_time = f"{tomorrow}T23:59:59Z"
                return self.handle_bulk_delete(start_time, end_time)
            elif "today" in query_lower:
                today = datetime.now().strftime('%Y-%m-%d')
                start_time = f"{today}T00:00:00Z"
                end_time = f"{today}T23:59:59Z"
                return self.handle_bulk_delete(start_time, end_time)
        
        if query.lower() in ['help', '?']:
            return """I can help you manage your calendar! Here are some examples of what you can say:

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
        
        try:
            # Get GPT's interpretation of the query
            response = self._get_gpt_response(query)
            if not response:
                return "I'm having trouble understanding your request. Please try again or type 'help' for examples."

            # Check if GPT wants to call a function
            if hasattr(response, 'tool_calls') and response.tool_calls:
                try:
                    tool_call = response.tool_calls[0]  # Get the first tool call
                    function_name = tool_call.function.name
                    function_args = eval(tool_call.function.arguments)
                    
                    # Call appropriate handler
                    if function_name == 'schedule_event':
                        return self.handle_schedule_event(function_args)
                    elif function_name == 'show_events':
                        return self.handle_show_events(function_args)
                    elif function_name == 'find_slots':
                        return self.handle_find_slots(function_args)
                    elif function_name == 'update_event':
                        return self.handle_update_event(function_args)
                    elif function_name == 'delete_event':
                        return self.handle_delete_event(function_args)
                    else:
                        return f"I don't know how to handle the operation: {function_name}. Please try rephrasing your request."
                except Exception as e:
                    print(f"Error processing function call: {str(e)}")
                    return "I understood your request but had trouble processing it. Please try again or rephrase your request."
            
            # If no function call but we have content, return it
            if hasattr(response, 'content') and response.content:
                return response.content
            
            # If we get here, something went wrong
            return "I'm not sure how to help with that. Type 'help' to see what I can do."
            
        except Exception as e:
            print(f"Error in process_query: {str(e)}")
            return "Something went wrong. Please try again or type 'help' for examples."

def main():
    """Main function to run the chatbot"""
    print("Calendar GPT Assistant")
    print("Type 'help' to see what I can do")
    print("Type 'quit' to exit")
    print("=" * 50)
    
    # Get OpenAI API key from environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        print("\nTo set up your OpenAI API key:")
        print("1. Get your API key from https://platform.openai.com/api-keys")
        print("2. Add it to your .env file:")
        print("   OPENAI_API_KEY=your-api-key-here")
        print("\nMake sure to set up billing at https://platform.openai.com/account/billing")
        return
    
    try:
        chatbot = CalendarGPTBot(api_key)
    except Exception as e:
        print(f"\nError initializing chatbot: {str(e)}")
        print("\nPlease check your OpenAI API key and make sure billing is set up.")
        return
    
    while True:
        try:
            query = input("\nYou: ").strip()
            
            if query.lower() in ['quit', 'exit', 'bye']:
                print("Goodbye!")
                break
            
            if not query:
                continue
            
            response = chatbot.process_query(query)
            print(f"\nBot: {response}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nBot: An error occurred: {str(e)}")
            print("Type 'help' to see available commands or 'quit' to exit.")

if __name__ == "__main__":
    main() 