#!/usr/bin/env python3

import unittest
from calendar_handler import CalendarHandler
from datetime import datetime, timedelta
import json
import os

class TestCalendarHandler(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.handler = CalendarHandler()
        print("\nStarting new test...")

    def test_1_authentication(self):
        """Test the authentication process"""
        print("\nSTEP 1: Authentication")
        print("Starting Google Calendar API authentication...")
        
        # Test authentication
        try:
            if os.path.exists('token.json'):
                print("Found existing token file, attempting to use...")
            
            result = self.handler.authenticate()
            self.assertTrue(result, "Authentication should succeed")
            print("Authentication successful!")
            
        except Exception as e:
            self.fail(f"Authentication failed with error: {str(e)}")

    def test_2_connection(self):
        """Test the connection to Google Calendar API"""
        print("\nSTEP 2: Connection Test")
        print("Testing API connection...")
        
        try:
            # Authenticate first
            self.handler.authenticate()
            
            # Get calendars to test connection
            calendars = self.handler.get_calendars()
            self.assertIsNotNone(calendars, "Should get calendar list")
            self.assertIsInstance(calendars, list, "Calendars should be returned as list")
            self.assertGreater(len(calendars), 0, "Should have at least one calendar")
            
            print(f"Connection successful! Found {len(calendars)} calendars")
            for i, calendar in enumerate(calendars[:3], 1):
                print(f"   {i}. {calendar.get('summary', 'Unnamed Calendar')}")
            if len(calendars) > 3:
                print(f"   ... and {len(calendars)-3} more")
            
        except Exception as e:
            self.fail(f"Connection test failed with error: {str(e)}")

    def test_3_calendar_data(self):
        """Test calendar data retrieval and storage"""
        print("\nSTEP 3: Fetching Calendar Data")
        print("\n============================================================")
        print("CALENDAR DATA SUMMARY")
        print("============================================================")
        
        try:
            # Authenticate first
            self.handler.authenticate()
            
            # Get calendars
            print("Fetching user calendars...")
            calendars = self.handler.get_calendars()
            print(f"Retrieved {len(calendars)} calendars")
            
            # Get primary calendar
            primary_calendar = next((cal for cal in calendars if cal.get('primary', False)), None)
            primary_id = primary_calendar['id'] if primary_calendar else None
            
            # Get events for primary calendar
            if primary_id:
                print(f"Fetching events from calendar '{primary_calendar['summary']}' for next 7 days...")
                start_time = datetime.now().isoformat() + 'Z'
                end_time = (datetime.now() + timedelta(days=7)).isoformat() + 'Z'
                
                events = self.handler.get_events(
                    start_time=start_time,
                    end_time=end_time,
                    calendar_id=primary_id
                )
                print(f"Retrieved {len(events)} events")
            
            # Print summary
            print(f"\nCalendars: {len(calendars)}")
            print(f"Events (next 7 days): {len(events) if 'events' in locals() else 0}")
            print(f"Primary Calendar: {primary_calendar['summary'] if primary_calendar else 'Not found'}\n")
            
            # Print all calendars
            print("All Calendars:")
            for i, calendar in enumerate(calendars, 1):
                suffix = " (Primary)" if calendar.get('primary', False) else ""
                print(f"   {i}. {calendar['summary']}{suffix}")
            
        except Exception as e:
            self.fail(f"Calendar data test failed with error: {str(e)}")

    def test_4_data_storage(self):
        """Test saving calendar data to file"""
        print("\nSTEP 4: Saving Data\n")
        
        try:
            # Authenticate first
            self.handler.authenticate()
            
            print("Saving calendar data to calendar_data.json...")
            
            # Get all calendars
            print("Fetching user calendars...")
            calendars = self.handler.get_calendars()
            print(f"Retrieved {len(calendars)} calendars")
            
            # Get events for each calendar
            all_events = []
            start_time = datetime.now().isoformat() + 'Z'
            end_time = (datetime.now() + timedelta(days=7)).isoformat() + 'Z'
            
            for calendar in calendars:
                print(f"Fetching events from calendar '{calendar['id']}' for next 7 days...")
                events = self.handler.get_events(
                    start_time=start_time,
                    end_time=end_time,
                    calendar_id=calendar['id']
                )
                print(f"Retrieved {len(events)} events")
                all_events.extend(events)
            
            # Prepare data for storage
            data = {
                'calendars': calendars,
                'events': all_events,
                'last_updated': datetime.now().isoformat()
            }
            
            # Save to file
            with open('calendar_data.json', 'w') as f:
                json.dump(data, f, indent=2)
            print("Data saved successfully to calendar_data.json")
            print(f"Summary: {len(calendars)} calendars, {len(all_events)} events")
            
        except Exception as e:
            self.fail(f"Data storage test failed with error: {str(e)}")

    def tearDown(self):
        """Clean up after each test method."""
        pass

if __name__ == '__main__':
    print("Google Calendar API Test")
    print("==================================================\n")
    
    # Run tests
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCalendarHandler)
    unittest.TextTestRunner(verbosity=0).run(suite)
    
    print("\nTest completed successfully!")
    print("\nGenerated files:")
    print("   - token.json (authentication token)")
    print("   - calendar_data.json (calendar data)") 