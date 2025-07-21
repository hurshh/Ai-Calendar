import os
import json
from typing import Dict, List
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
import pytz
from google.auth.transport.requests import Request

class GoogleCalendarTest:
    """
    Simple test class to connect with GCP and fetch user calendar data
    """
    
    def __init__(self):
        # Google Calendar API scopes
        self.SCOPES = [
            'https://www.googleapis.com/auth/calendar.readonly',
            'https://www.googleapis.com/auth/calendar.events.readonly'
        ]
        
        # File paths
        self.credentials_file = 'credentials.json'
        self.token_file = 'token.json'
        
        # Service instance
        self.service = None
        
    def authenticate(self) -> bool:
        """
        Authenticate with Google Calendar API
        Returns True if successful, False otherwise
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
    
    def test_connection(self) -> bool:
        """
        Test the connection by making a simple API call
        """
        if not self.service:
            print("No service available. Please authenticate first.")
            return False
        
        try:
            print("Testing API connection...")
            # Make a simple call to list calendars
            calendar_list = self.service.calendarList().list().execute()
            calendars = calendar_list.get('items', [])
            
            print(f"Connection successful! Found {len(calendars)} calendars")
            
            # Show calendar names
            for i, calendar in enumerate(calendars[:3]):
                print(f"   {i+1}. {calendar.get('summary', 'Unknown')}")
            
            if len(calendars) > 3:
                print(f"   ... and {len(calendars) - 3} more")
            
            return True
            
        except HttpError as error:
            print(f"API connection failed: {error}")
            return False
    
    def get_user_calendars(self) -> List[Dict]:
        """
        Get all calendars accessible to the user
        """
        if not self.service:
            print("No service available. Please authenticate first.")
            return []
        
        try:
            print("Fetching user calendars...")
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
            
            print(f"Retrieved {len(calendar_data)} calendars")
            return calendar_data
            
        except HttpError as error:
            print(f"Error fetching calendars: {error}")
            return []
    
    def get_calendar_events(self, calendar_id: str = 'primary', days: int = 7) -> List[Dict]:
        """
        Get events from a specific calendar
        """
        if not self.service:
            print("No service available. Please authenticate first.")
            return []
        
        try:
            print(f"Fetching events from calendar '{calendar_id}' for next {days} days...")
            
            # Calculate time range
            now = datetime.now(pytz.UTC)
            time_min = now.isoformat()
            time_max = (now + timedelta(days=days)).isoformat()
            
            events_result = self.service.events().list(
                calendarId=calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                maxResults=20,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            event_data = []
            for event in events:
                start = event.get('start', {})
                end = event.get('end', {})
                
                event_info = {
                    'id': event.get('id'),
                    'summary': event.get('summary', 'No Title'),
                    'description': event.get('description', ''),
                    'location': event.get('location', ''),
                    'start_time': start.get('dateTime') or start.get('date'),
                    'end_time': end.get('dateTime') or end.get('date'),
                    'all_day': 'date' in start,
                    'attendees_count': len(event.get('attendees', [])),
                    'organizer': event.get('organizer', {}).get('email', ''),
                    'htmlLink': event.get('htmlLink', ''),
                    'hangoutLink': event.get('hangoutLink', '')
                }
                event_data.append(event_info)
            
            print(f"Retrieved {len(event_data)} events")
            return event_data
            
        except HttpError as error:
            print(f"Error fetching events: {error}")
            return []
    
    def display_calendar_summary(self):
        """
        Display a summary of the user's calendar data
        """
        print("\n" + "="*60)
        print("CALENDAR DATA SUMMARY")
        print("="*60)
        
        # Get calendars
        calendars = self.get_user_calendars()
        
        if not calendars:
            print("No calendars found")
            return
        
        # Get events from primary calendar
        primary_calendar = next((cal for cal in calendars if cal.get('primary')), calendars[0])
        events = self.get_calendar_events(primary_calendar['id'])
        
        # Display summary
        print(f"\nCalendars: {len(calendars)}")
        print(f"Events (next 7 days): {len(events)}")
        print(f"Primary Calendar: {primary_calendar['summary']}")
        
        # Show recent events
        if events:
            print(f"\nRecent Events:")
            for i, event in enumerate(events[:5]):
                start_time = event['start_time']
                if 'T' in start_time:
                    # Parse datetime
                    dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                    time_str = dt.strftime("%I:%M %p")
                else:
                    time_str = "All Day"
                
                print(f"   {i+1}. {event['summary']} - {time_str}")
        
        # Show all calendars
        print(f"\nAll Calendars:")
        for i, calendar in enumerate(calendars):
            primary_marker = " (Primary)" if calendar.get('primary') else ""
            print(f"   {i+1}. {calendar['summary']}{primary_marker}")
    
    def save_data_to_file(self, filename: str = 'calendar_data.json'):
        """
        Save all calendar data to a JSON file
        """
        print(f"\nSaving calendar data to {filename}...")
        
        try:
            calendars = self.get_user_calendars()
            all_events = {}
            
            # Get events for each calendar
            for calendar in calendars:
                calendar_id = calendar['id']
                events = self.get_calendar_events(calendar_id)
                all_events[calendar_id] = events
            
            # Compile data
            data = {
                'export_timestamp': datetime.now().isoformat(),
                'calendars': calendars,
                'events': all_events,
                'summary': {
                    'total_calendars': len(calendars),
                    'total_events': sum(len(events) for events in all_events.values()),
                    'primary_calendar': next((cal['id'] for cal in calendars if cal.get('primary')), None)
                }
            }
            
            # Save to file
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"Data saved successfully to {filename}")
            print(f"Summary: {data['summary']['total_calendars']} calendars, {data['summary']['total_events']} events")
            
        except Exception as e:
            print(f"Error saving data: {e}")

def main():
    """
    Main test function
    """
    print("Google Calendar API Test")
    print("="*50)
    
    # Create test instance
    test = GoogleCalendarTest()
    
    # Step 1: Authenticate
    print("\nSTEP 1: Authentication")
    if not test.authenticate():
        print("Authentication failed. Exiting.")
        return
    
    # Step 2: Test connection
    print("\nSTEP 2: Connection Test")
    if not test.test_connection():
        print("Connection test failed. Exiting.")
        return
    
    # Step 3: Fetch and display data
    print("\nSTEP 3: Fetching Calendar Data")
    test.display_calendar_summary()
    
    # Step 4: Save data
    print("\nSTEP 4: Saving Data")
    test.save_data_to_file()
    
    print("\nTest completed successfully!")
    print("\nGenerated files:")
    print("   - token.json (authentication token)")
    print("   - calendar_data.json (calendar data)")

if __name__ == "__main__":
    main()