#!/usr/bin/env python3
"""
Calendar Handler - Comprehensive Google Calendar Management

This module provides a complete calendar management system with:
- OAuth 2.0 authentication
- Event creation and deletion
- Availability checking
- Calendar management
- Conflict detection

Usage:
    handler = CalendarHandler()
    handler.authenticate()
    handler.add_event(title="Meeting", start_time="2024-01-15T10:00:00", duration_minutes=60)
    handler.check_availability(start_time="2024-01-15T10:00:00", end_time="2024-01-15T11:00:00")
    handler.delete_event(event_id="event_id_here")
"""

import os
import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import pytz
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request

class CalendarHandler:
    """
    Comprehensive Google Calendar management handler
    """
    
    def __init__(self, credentials_file: str = 'credentials.json', token_file: str = 'token.json'):
        """
        Initialize the Calendar Handler
        
        Args:
            credentials_file: Path to Google Cloud credentials file
            token_file: Path to store OAuth tokens
        """
        # Google Calendar API scopes - Full access for event management
        self.SCOPES = [
            'https://www.googleapis.com/auth/calendar',
            'https://www.googleapis.com/auth/calendar.events'
        ]
        
        # File paths
        self.credentials_file = credentials_file
        self.token_file = token_file
        
        # Service instance
        self.service = None
        
        # Default calendar ID
        self.default_calendar_id = 'primary'
        
        # Default timezone
        self.timezone = 'UTC'
    
    def authenticate(self) -> bool:
        """
        Authenticate with Google Calendar API using OAuth 2.0
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        print("Starting Google Calendar API authentication...")
        
        creds = None
        
        # Check if we have a saved token
        if os.path.exists(self.token_file):
            print("Found existing token file, attempting to use...")
            try:
                creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)
                print("Loaded existing credentials")
            except Exception as e:
                print(f"Error loading token: {e}")
                creds = None
        
        # If no valid credentials, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("Refreshing expired token...")
                try:
                    creds.refresh(Request())
                    print("Token refreshed successfully")
                except Exception as e:
                    print(f"Failed to refresh token: {e}")
                    creds = None
            
            # If still no valid credentials, start OAuth flow
            if not creds:
                if not os.path.exists(self.credentials_file):
                    print(f"Credentials file '{self.credentials_file}' not found!")
                    print("\nSetup Instructions:")
                    print("1. Go to https://console.cloud.google.com/")
                    print("2. Create a project or select existing one")
                    print("3. Enable Google Calendar API")
                    print("4. Create OAuth 2.0 credentials (Desktop application)")
                    print("5. Download credentials.json and place it in this directory")
                    return False
                
                print("Starting OAuth 2.0 authentication flow...")
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, 
                        self.SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                    print("OAuth authentication successful!")
                except Exception as e:
                    print(f"OAuth authentication failed: {e}")
                    return False
            
            # Save the credentials for next time
            try:
                with open(self.token_file, 'w') as token:
                    token.write(creds.to_json())
                print("Credentials saved to token.json")
            except Exception as e:
                print(f"Could not save credentials: {e}")
        
        # Build the service
        try:
            self.service = build('calendar', 'v3', credentials=creds)
            print("Google Calendar API service created successfully!")
            return True
        except Exception as e:
            print(f"Failed to create service: {e}")
            return False
    
    def get_calendars(self) -> List[Dict]:
        """
        Get all accessible calendars
        
        Returns:
            List of calendar dictionaries
        """
        if not self.service:
            print("No service available. Please authenticate first.")
            return []
        
        try:
            calendar_list = self.service.calendarList().list().execute()
            calendars = calendar_list.get('items', [])
            
            calendar_data = []
            for calendar in calendars:
                calendar_info = {
                    'id': calendar.get('id'),
                    'summary': calendar.get('summary', 'Unknown'),
                    'description': calendar.get('description', ''),
                    'timeZone': calendar.get('timeZone', 'UTC'),
                    'primary': calendar.get('primary', False),
                    'selected': calendar.get('selected', True),
                    'accessRole': calendar.get('accessRole', '')
                }
                calendar_data.append(calendar_info)
            
            return calendar_data
            
        except HttpError as error:
            print(f"Error fetching calendars: {error}")
            return []
    
    def set_default_calendar(self, calendar_id: str) -> bool:
        """
        Set the default calendar for operations
        
        Args:
            calendar_id: Calendar ID to set as default
            
        Returns:
            bool: True if successful, False otherwise
        """
        calendars = self.get_calendars()
        calendar_ids = [cal['id'] for cal in calendars]
        
        if calendar_id in calendar_ids:
            self.default_calendar_id = calendar_id
            print(f"Default calendar set to: {calendar_id}")
            return True
        else:
            print(f"Calendar ID '{calendar_id}' not found in accessible calendars")
            return False
    
    def add_event(self, 
                  title: str,
                  start_time: str,
                  duration_minutes: int = 60,
                  description: str = "",
                  location: str = "",
                  attendees: List[str] = None,
                  calendar_id: str = None,
                  all_day: bool = False,
                  reminders: Dict = None) -> Optional[str]:
        """
        Add a new event to the calendar
        
        Args:
            title: Event title
            start_time: Start time in ISO format (e.g., "2024-01-15T10:00:00")
            duration_minutes: Event duration in minutes
            description: Event description
            location: Event location
            attendees: List of attendee email addresses
            calendar_id: Calendar ID (uses default if None)
            all_day: Whether this is an all-day event
            reminders: Custom reminders configuration
            
        Returns:
            str: Event ID if successful, None otherwise
        """
        if not self.service:
            print("No service available. Please authenticate first.")
            return None
        
        # Use default calendar if none specified
        if calendar_id is None:
            calendar_id = self.default_calendar_id
        
        try:
            # Parse start time
            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            
            # Calculate end time
            if all_day:
                end_dt = start_dt + timedelta(days=1)
                start_event = {'date': start_dt.date().isoformat()}
                end_event = {'date': end_dt.date().isoformat()}
            else:
                end_dt = start_dt + timedelta(minutes=duration_minutes)
                start_event = {'dateTime': start_dt.isoformat(), 'timeZone': self.timezone}
                end_event = {'dateTime': end_dt.isoformat(), 'timeZone': self.timezone}
            
            # Build event object
            event = {
                'summary': title,
                'description': description,
                'location': location,
                'start': start_event,
                'end': end_event
            }
            
            # Add attendees if provided
            if attendees:
                event['attendees'] = [{'email': email} for email in attendees]
            
            # Add reminders if provided
            if reminders:
                event['reminders'] = reminders
            else:
                # Default reminders
                event['reminders'] = {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                        {'method': 'popup', 'minutes': 10}        # 10 minutes before
                    ]
                }
            
            # Insert the event
            event_result = self.service.events().insert(
                calendarId=calendar_id,
                body=event,
                sendUpdates='all' if attendees else 'none'
            ).execute()
            
            event_id = event_result.get('id')
            print(f"Event '{title}' created successfully with ID: {event_id}")
            return event_id
            
        except HttpError as error:
            print(f"Error creating event: {error}")
            return None
        except Exception as e:
            print(f"Error creating event: {e}")
            return None
    
    def delete_event(self, event_id: str, calendar_id: str = None) -> bool:
        """
        Delete an event from the calendar
        
        Args:
            event_id: ID of the event to delete
            calendar_id: Calendar ID (uses default if None)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.service:
            print("No service available. Please authenticate first.")
            return False
        
        # Use default calendar if none specified
        if calendar_id is None:
            calendar_id = self.default_calendar_id
        
        try:
            self.service.events().delete(
                calendarId=calendar_id,
                eventId=event_id,
                sendUpdates='all'
            ).execute()
            
            print(f"Event {event_id} deleted successfully")
            return True
            
        except HttpError as error:
            print(f"Error deleting event: {error}")
            return False
    
    def update_event(self, 
                    event_id: str,
                    title: str = None,
                    start_time: str = None,
                    end_time: str = None,
                    description: str = None,
                    location: str = None,
                    attendees: List[str] = None,
                    calendar_id: str = None) -> bool:
        """
        Update an existing event
        
        Args:
            event_id: ID of the event to update
            title: New event title
            start_time: New start time
            end_time: New end time
            description: New description
            location: New location
            attendees: New list of attendees
            calendar_id: Calendar ID (uses default if None)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.service:
            print("No service available. Please authenticate first.")
            return False
        
        # Use default calendar if none specified
        if calendar_id is None:
            calendar_id = self.default_calendar_id
        
        try:
            # Get existing event
            event = self.service.events().get(
                calendarId=calendar_id,
                eventId=event_id
            ).execute()
            
            # Update fields if provided
            if title:
                event['summary'] = title
            if description:
                event['description'] = description
            if location:
                event['location'] = location
            if start_time:
                start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                event['start'] = {'dateTime': start_dt.isoformat(), 'timeZone': self.timezone}
            if end_time:
                end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
                event['end'] = {'dateTime': end_dt.isoformat(), 'timeZone': self.timezone}
            if attendees:
                event['attendees'] = [{'email': email} for email in attendees]
            
            # Update the event
            updated_event = self.service.events().update(
                calendarId=calendar_id,
                eventId=event_id,
                body=event,
                sendUpdates='all'
            ).execute()
            
            print(f"Event {event_id} updated successfully")
            return True
            
        except HttpError as error:
            print(f"Error updating event: {error}")
            return False
    
    def get_event(self, event_id: str, calendar_id: str = None) -> Optional[Dict]:
        """
        Get a specific event by ID
        
        Args:
            event_id: ID of the event to retrieve
            calendar_id: Calendar ID (uses default if None)
            
        Returns:
            Dict: Event data if found, None otherwise
        """
        if not self.service:
            print("No service available. Please authenticate first.")
            return None
        
        # Use default calendar if none specified
        if calendar_id is None:
            calendar_id = self.default_calendar_id
        
        try:
            event = self.service.events().get(
                calendarId=calendar_id,
                eventId=event_id
            ).execute()
            
            return event
            
        except HttpError as error:
            print(f"Error retrieving event: {error}")
            return None
    
    def get_events(self, 
                   start_time: str = None,
                   end_time: str = None,
                   calendar_id: str = None,
                   max_results: int = 50) -> List[Dict]:
        """
        Get events from a calendar within a time range
        
        Args:
            start_time: Start time in ISO format (defaults to now)
            end_time: End time in ISO format (defaults to 7 days from now)
            calendar_id: Calendar ID (uses default if None)
            max_results: Maximum number of events to return
            
        Returns:
            List of event dictionaries
        """
        if not self.service:
            print("No service available. Please authenticate first.")
            return []
        
        # Use default calendar if none specified
        if calendar_id is None:
            calendar_id = self.default_calendar_id
        
        try:
            # Set default time range if not provided
            if start_time is None:
                start_time = datetime.now(pytz.UTC).isoformat()
            if end_time is None:
                end_time = (datetime.now(pytz.UTC) + timedelta(days=7)).isoformat()
            
            events_result = self.service.events().list(
                calendarId=calendar_id,
                timeMin=start_time,
                timeMax=end_time,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            return events
            
        except HttpError as error:
            print(f"Error fetching events: {error}")
            return []
    
    def check_availability(self, 
                          start_time: str,
                          end_time: str,
                          calendar_id: str = None) -> Tuple[bool, List[Dict]]:
        """
        Check if a time slot is available (no conflicts)
        
        Args:
            start_time: Start time in ISO format
            end_time: End time in ISO format
            calendar_id: Calendar ID (uses default if None)
            
        Returns:
            Tuple[bool, List[Dict]]: (is_available, conflicting_events)
        """
        if not self.service:
            print("No service available. Please authenticate first.")
            return False, []
        
        # Use default calendar if none specified
        if calendar_id is None:
            calendar_id = self.default_calendar_id
        
        try:
            # Get events in the time range
            events = self.get_events(start_time, end_time, calendar_id)
            
            # Check for conflicts
            conflicting_events = []
            for event in events:
                event_start = event.get('start', {}).get('dateTime') or event.get('start', {}).get('date')
                event_end = event.get('end', {}).get('dateTime') or event.get('end', {}).get('date')
                
                # Convert to datetime for comparison
                if 'T' in event_start:
                    event_start_dt = datetime.fromisoformat(event_start.replace('Z', '+00:00'))
                    event_end_dt = datetime.fromisoformat(event_end.replace('Z', '+00:00'))
                    requested_start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                    requested_end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
                    
                    # Check for overlap
                    if (event_start_dt < requested_end_dt and event_end_dt > requested_start_dt):
                        conflicting_events.append(event)
            
            is_available = len(conflicting_events) == 0
            
            if is_available:
                print(f"Time slot {start_time} to {end_time} is available")
            else:
                print(f"Time slot {start_time} to {end_time} has {len(conflicting_events)} conflicts")
            
            return is_available, conflicting_events
            
        except Exception as e:
            print(f"Error checking availability: {e}")
            return False, []
    
    def find_available_slots(self, 
                            date: str,
                            duration_minutes: int = 60,
                            start_hour: int = 9,
                            end_hour: int = 17,
                            calendar_id: str = None) -> List[Dict]:
        """
        Find available time slots on a specific date
        
        Args:
            date: Date in YYYY-MM-DD format
            duration_minutes: Duration of desired slot in minutes
            start_hour: Start hour (24-hour format)
            end_hour: End hour (24-hour format)
            calendar_id: Calendar ID (uses default if None)
            
        Returns:
            List of available time slots
        """
        if not self.service:
            print("No service available. Please authenticate first.")
            return []
        
        # Use default calendar if none specified
        if calendar_id is None:
            calendar_id = self.default_calendar_id
        
        try:
            # Create time range for the entire day in UTC
            start_of_day = f"{date}T00:00:00.000Z"
            end_of_day = f"{date}T23:59:59.999Z"
            
            # Get all events for the day
            events = self.get_events(start_of_day, end_of_day, calendar_id)
            
            # Create busy time ranges
            busy_ranges = []
            for event in events:
                event_start = event.get('start', {}).get('dateTime') or event.get('start', {}).get('date')
                event_end = event.get('end', {}).get('dateTime') or event.get('end', {}).get('date')
                
                if 'T' in event_start:  # Skip all-day events
                    # Convert to UTC
                    start_dt = datetime.fromisoformat(event_start.replace('Z', '+00:00'))
                    end_dt = datetime.fromisoformat(event_end.replace('Z', '+00:00'))
                    busy_ranges.append((start_dt, end_dt))
            
            # Sort busy ranges by start time
            busy_ranges.sort(key=lambda x: x[0])
            
            # Find available slots
            available_slots = []
            
            # Create timezone aware datetime objects
            tz = pytz.UTC
            current_time = datetime.strptime(f"{date}T{start_hour:02d}:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=tz)
            end_time = datetime.strptime(f"{date}T{end_hour:02d}:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=tz)
            
            while current_time + timedelta(minutes=duration_minutes) <= end_time:
                # Check if this slot conflicts with any busy time
                slot_available = True
                slot_end_time = current_time + timedelta(minutes=duration_minutes)
                
                for busy_start, busy_end in busy_ranges:
                    if (busy_start < slot_end_time and busy_end > current_time):
                        slot_available = False
                        break
                
                if slot_available:
                    available_slots.append({
                        'start_time': current_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'end_time': slot_end_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'duration_minutes': duration_minutes
                    })
                
                # Move to next 30-minute slot
                current_time += timedelta(minutes=30)
            
            print(f"Found {len(available_slots)} available {duration_minutes}-minute slots on {date}")
            return available_slots
            
        except Exception as e:
            print(f"Error finding available slots: {e}")
            return []
    
    def get_free_busy(self, 
                     start_time: str,
                     end_time: str,
                     calendar_ids: List[str] = None) -> Dict:
        """
        Get free/busy information for specified calendars
        
        Args:
            start_time: Start time in ISO format
            end_time: End time in ISO format
            calendar_ids: List of calendar IDs (uses default if None)
            
        Returns:
            Dict: Free/busy information
        """
        if not self.service:
            print("No service available. Please authenticate first.")
            return {}
        
        # Use default calendar if none specified
        if calendar_ids is None:
            calendar_ids = [self.default_calendar_id]
        
        try:
            body = {
                'timeMin': start_time,
                'timeMax': end_time,
                'items': [{'id': cal_id} for cal_id in calendar_ids]
            }
            
            free_busy_result = self.service.freebusy().query(body=body).execute()
            return free_busy_result
            
        except HttpError as error:
            print(f"Error fetching free/busy data: {error}")
            return {}

def main():
    """
    Example usage of the CalendarHandler
    """
    print("Calendar Handler Example")
    print("="*50)
    
    # Create handler instance
    handler = CalendarHandler()
    
    # Authenticate
    if not handler.authenticate():
        print("Authentication failed. Exiting.")
        return
    
    # Get calendars
    calendars = handler.get_calendars()
    print(f"Found {len(calendars)} calendars")
    
    # Example: Add an event
    event_id = handler.add_event(
        title="Test Meeting",
        start_time="2024-01-20T10:00:00",
        duration_minutes=60,
        description="This is a test meeting",
        location="Conference Room A",
        attendees=["test@example.com"]
    )
    
    if event_id:
        # Check availability
        is_available, conflicts = handler.check_availability(
            start_time="2024-01-20T10:00:00",
            end_time="2024-01-20T11:00:00"
        )
        
        # Find available slots
        available_slots = handler.find_available_slots(
            date="2024-01-20",
            duration_minutes=60
        )
        
        # Delete the test event
        handler.delete_event(event_id)
    
    print("Example completed!")

if __name__ == "__main__":
    main() 