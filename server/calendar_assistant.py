#!/usr/bin/env python3

import os
import openai
from datetime import datetime, timedelta
import re
from calendar_handler import CalendarHandler
import json

class CalendarAssistant:
    def __init__(self):
        # Initialize OpenAI API
        self.openai = openai
        self.openai.api_key = os.getenv('OPENAI_API_KEY')
        if not self.openai.api_key:
            raise ValueError("Please set the OPENAI_API_KEY environment variable")

        # Initialize Calendar Handler
        self.calendar = CalendarHandler()
        if not self.calendar.authenticate():
            raise ValueError("Failed to authenticate with Google Calendar")

        # Store conversation history
        self.conversation_history = [
            {"role": "system", "content": """
            You are a helpful calendar assistant that helps users manage their Google Calendar.
            You can help with:
            1. Adding new events
            2. Deleting events
            3. Listing upcoming events
            4. Finding available time slots
            5. Checking schedule conflicts
            
            Extract relevant information from user messages and help manage their calendar.
            Always confirm details before making changes.
            """}
        ]

    def extract_date_time(self, text):
        """Extract date and time from natural language text using OpenAI."""
        prompt = f"""
        Extract the date and time information from the following text. 
        If multiple dates/times are mentioned, identify the event start time.
        Return the result in JSON format with keys: "date" (YYYY-MM-DD) and "time" (HH:MM).
        If no specific time is mentioned, use None for time.
        Text: {text}
        """
        
        response = self.openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        try:
            result = json.loads(response.choices[0].message.content)
            return result.get("date"), result.get("time")
        except:
            return None, None

    def extract_event_details(self, text):
        """Extract event details from natural language text using OpenAI."""
        prompt = f"""
        Extract event details from the following text.
        Return the result in JSON format with keys:
        - "title": event title
        - "duration": duration in minutes (default to 60 if not specified)
        - "description": event description (or empty string)
        - "location": location (or empty string)
        - "attendees": list of email addresses (or empty list)
        
        Text: {text}
        """
        
        response = self.openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        try:
            return json.loads(response.choices[0].message.content)
        except:
            return None

    def process_message(self, user_message):
        """Process user message and take appropriate action."""
        # Add user message to conversation history
        self.conversation_history.append({"role": "user", "content": user_message})
        
        # Get intent and action from OpenAI
        response = self.openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                *self.conversation_history,
                {"role": "system", "content": """
                Determine the user's intent. Possible intents are:
                - add_event
                - delete_event
                - list_events
                - check_availability
                - help
                Return ONLY the intent as a single word.
                """}
            ]
        )
        
        intent = response.choices[0].message.content.strip().lower()
        
        try:
            if intent == "add_event":
                return self._handle_add_event(user_message)
            elif intent == "delete_event":
                return self._handle_delete_event(user_message)
            elif intent == "list_events":
                return self._handle_list_events(user_message)
            elif intent == "check_availability":
                return self._handle_check_availability(user_message)
            else:
                return self._get_help_message()
        except Exception as e:
            return f"I encountered an error: {str(e)}"

    def _handle_add_event(self, message):
        """Handle adding a new event."""
        # Extract date and time
        date, time = self.extract_date_time(message)
        if not date:
            return "I couldn't understand the date and time. Please specify when the event should occur."

        # Extract other event details
        details = self.extract_event_details(message)
        if not details:
            return "I couldn't understand the event details. Please provide more information."

        # Confirm with user
        confirmation = f"""
        I'll add an event with these details:
        - Title: {details['title']}
        - Date: {date}
        - Time: {time or 'Not specified'}
        - Duration: {details['duration']} minutes
        - Description: {details['description']}
        - Location: {details['location']}
        - Attendees: {', '.join(details['attendees']) if details['attendees'] else 'None'}
        
        Should I proceed? (yes/no)
        """
        
        self.conversation_history.append({"role": "assistant", "content": confirmation})
        return confirmation

    def _handle_delete_event(self, message):
        """Handle deleting an event."""
        # First list recent events
        events = self.calendar.get_events(max_results=5)
        
        event_list = "Recent events:\n"
        for event in events:
            start = event.get('start', {}).get('dateTime', event.get('start', {}).get('date'))
            event_list += f"- {event.get('summary')} (ID: {event.get('id')})\n  Start: {start}\n"
        
        return f"{event_list}\nPlease provide the event ID you want to delete."

    def _handle_list_events(self, message):
        """Handle listing events."""
        # Extract date range if specified
        date, _ = self.extract_date_time(message)
        
        if date:
            start_time = f"{date}T00:00:00"
            end_time = f"{date}T23:59:59"
        else:
            # Default to upcoming events
            start_time = datetime.now().isoformat()
            end_time = (datetime.now() + timedelta(days=7)).isoformat()
        
        events = self.calendar.get_events(start_time=start_time, end_time=end_time)
        
        if not events:
            return "No events found for the specified period."
        
        response = "Here are the events:\n"
        for event in events:
            start = event.get('start', {}).get('dateTime', event.get('start', {}).get('date'))
            response += f"- {event.get('summary')}\n  Start: {start}\n"
        
        return response

    def _handle_check_availability(self, message):
        """Handle checking availability."""
        date, time = self.extract_date_time(message)
        if not date or not time:
            return "Please specify the date and time you want to check."
        
        start_time = f"{date}T{time}:00"
        end_time = (datetime.fromisoformat(start_time) + timedelta(hours=1)).isoformat()
        
        is_available, conflicts = self.calendar.check_availability(start_time, end_time)
        
        if is_available:
            return f"The time slot on {date} at {time} is available!"
        else:
            response = f"The time slot is not available. Conflicts:\n"
            for conflict in conflicts:
                start = conflict.get('start', {}).get('dateTime', conflict.get('start', {}).get('date'))
                response += f"- {conflict.get('summary')}\n  Start: {start}\n"
            return response

    def _get_help_message(self):
        """Return help message."""
        return """
        I can help you manage your calendar! Here's what I can do:
        
        1. Add events:
           "Schedule a team meeting tomorrow at 2pm for 90 minutes"
           
        2. Delete events:
           "Delete my meeting with John"
           
        3. List events:
           "What meetings do I have today?"
           "Show my schedule for next week"
           
        4. Check availability:
           "Am I free tomorrow at 3pm?"
           "Find me an available slot on Friday"
           
        Just let me know what you'd like to do!
        """

    def confirm_action(self, user_response):
        """Handle user confirmation for actions."""
        if user_response.lower() in ['yes', 'y', 'sure', 'okay']:
            # Extract the last proposed action from conversation history
            last_action = next((msg for msg in reversed(self.conversation_history) 
                              if msg["role"] == "assistant" and "I'll add an event" in msg["content"]), None)
            
            if last_action:
                # Parse the confirmation message to extract details
                lines = last_action["content"].split('\n')
                details = {}
                for line in lines:
                    if ': ' in line:
                        key, value = line.split(': ', 1)
                        details[key.strip('- ')] = value

                # Add the event
                start_time = f"{details['Date']}T{details['Time'].replace('Not specified', '00:00')}:00"
                
                event_id = self.calendar.add_event(
                    title=details['Title'],
                    start_time=start_time,
                    duration_minutes=int(details['Duration'].split()[0]),
                    description=details['Description'],
                    location=details['Location'],
                    attendees=details['Attendees'].split(', ') if details['Attendees'] != 'None' else None
                )
                
                if event_id:
                    return "Event has been added successfully!"
                else:
                    return "Failed to add the event. Please try again."
            
            return "I couldn't find the action to confirm. Please try your request again."
        else:
            return "Action cancelled. What else would you like to do?"

def main():
    """Main function to run the calendar assistant."""
    try:
        assistant = CalendarAssistant()
        print("Calendar Assistant: Hello! How can I help you manage your calendar today?")
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Calendar Assistant: Goodbye!")
                break
            
            # Check if this is a confirmation response
            if user_input.lower() in ['yes', 'y', 'no', 'n', 'sure', 'okay', 'cancel']:
                response = assistant.confirm_action(user_input)
            else:
                response = assistant.process_message(user_input)
            
            print("Calendar Assistant:", response)
    except Exception as e:
        print(f"Calendar Assistant: An error occurred: {str(e)}")
        print("Calendar Assistant: Please make sure you have set up your OpenAI API key and Google Calendar credentials correctly.")

if __name__ == "__main__":
    main() 