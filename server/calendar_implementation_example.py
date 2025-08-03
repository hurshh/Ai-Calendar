#!/usr/bin/env python3

from calendar_handler import CalendarHandler
from datetime import datetime, timedelta
import json
from pprint import pprint

def format_timestamp(dt):
    """Format datetime to RFC3339 timestamp"""
    return dt.strftime('%Y-%m-%dT%H:%M:%S.000Z')

def main():
    print("Calendar Handler Implementation Examples")
    print("=" * 50)

    # Initialize handler
    handler = CalendarHandler()
    
    try:
        # 1. Authentication
        print("\n1. Authentication")
        print("-" * 20)
        if handler.authenticate():
            print("✓ Authentication successful")
        else:
            print("✗ Authentication failed")
            return

        # 2. Calendar Operations
        print("\n2. Calendar Operations")
        print("-" * 20)
        
        # Get all calendars
        print("\na) Getting all calendars:")
        calendars = handler.get_calendars()
        print(f"Found {len(calendars)} calendars:")
        for cal in calendars:
            print(f"  - {cal['summary']} ({cal['id']})")
            if cal.get('primary', False):
                primary_calendar_id = cal['id']
                print("    ↳ This is your primary calendar")

        # 3. Event Management
        print("\n3. Event Management")
        print("-" * 20)

        # Create timestamps for examples
        now = datetime.utcnow()  # Use UTC time
        tomorrow = now + timedelta(days=1)
        next_week = now + timedelta(days=7)
        
        # Format timestamps for API
        tomorrow_10am = tomorrow.replace(hour=10, minute=0, second=0, microsecond=0)
        tomorrow_11am = tomorrow.replace(hour=11, minute=0, second=0, microsecond=0)
        
        # Format timestamps properly
        start_time = format_timestamp(tomorrow_10am)
        end_time = format_timestamp(tomorrow_11am)

        # a) Add Event
        print("\na) Adding a new event:")
        event_id = handler.add_event(
            title="Team Sync Meeting",
            start_time=start_time,
            duration_minutes=60,
            description="Weekly team sync meeting to discuss progress",
            location="Conference Room A",
            attendees=["example@example.com"],  # Replace with real email
            calendar_id=primary_calendar_id
        )
        print(f"✓ Created event with ID: {event_id}")

        # b) Get Event Details
        print("\nb) Getting event details:")
        event = handler.get_events(
            start_time=start_time,
            end_time=end_time,
            calendar_id=primary_calendar_id
        )
        if event:
            print("Event details:")
            pprint(event[0])

        # c) Update Event
        print("\nc) Updating event:")
        updated = handler.update_event(
            event_id=event_id,
            title="Updated: Team Sync Meeting",
            description="Updated description: Weekly team sync with project updates",
            calendar_id=primary_calendar_id
        )
        print("✓ Event updated successfully" if updated else "✗ Update failed")

        # 4. Availability Checking
        print("\n4. Availability Checking")
        print("-" * 20)

        # a) Check specific time slot
        print("\na) Checking specific time slot:")
        is_available, conflicts = handler.check_availability(
            start_time=start_time,
            end_time=end_time,
            calendar_id=primary_calendar_id
        )
        print(f"Time slot is {'available' if is_available else 'not available'}")
        if conflicts:
            print("Conflicting events:")
            for conflict in conflicts:
                print(f"  - {conflict['summary']}")

        # b) Find available slots
        print("\nb) Finding available slots:")
        # Create start and end times for the day in UTC
        tomorrow_start = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow_end = tomorrow.replace(hour=23, minute=59, second=59, microsecond=0)
        
        # Format timestamps properly
        day_start = format_timestamp(tomorrow_start)
        day_end = format_timestamp(tomorrow_end)
        
        # Get events for the entire day
        events = handler.get_events(
            start_time=day_start,
            end_time=day_end,
            calendar_id=primary_calendar_id
        )
        
        # Print any existing events
        if events:
            print("\nExisting events for tomorrow:")
            for event in events:
                start = event.get('start', {}).get('dateTime', 'Unknown')
                end = event.get('end', {}).get('dateTime', 'Unknown')
                print(f"  - {event.get('summary')}: {start} to {end}")
        
        # Find available slots
        tomorrow_date = tomorrow.strftime("%Y-%m-%d")
        available_slots = handler.find_available_slots(
            date=tomorrow_date,
            duration_minutes=60,
            start_hour=9,
            end_hour=17,
            calendar_id=primary_calendar_id
        )
        print("\nAvailable 60-minute slots tomorrow:")
        for slot in available_slots[:3]:  # Show first 3 slots
            print(f"  - {slot['start_time']} to {slot['end_time']}")
        if len(available_slots) > 3:
            print(f"    ... and {len(available_slots)-3} more slots")

        # 5. Cleanup - Delete Event
        print("\n5. Cleanup")
        print("-" * 20)
        print("\nDeleting test event:")
        deleted = handler.delete_event(
            event_id=event_id,
            calendar_id=primary_calendar_id
        )
        print("✓ Event deleted successfully" if deleted else "✗ Deletion failed")

        # 6. Save Calendar Data
        print("\n6. Data Storage")
        print("-" * 20)
        print("\nSaving calendar data to file:")
        
        # Get events for next week
        next_week_time = format_timestamp(next_week)
        now_time = format_timestamp(now)
        
        events = handler.get_events(
            start_time=now_time,
            end_time=next_week_time,
            calendar_id=primary_calendar_id
        )
        
        # Prepare data for storage
        data = {
            'calendars': calendars,
            'upcoming_events': events,
            'last_updated': now.isoformat()
        }
        
        # Save to file
        with open('calendar_data.json', 'w') as f:
            json.dump(data, f, indent=2)
        print("✓ Calendar data saved to calendar_data.json")

    except Exception as e:
        print(f"\n✗ Error occurred: {str(e)}")
    
    print("\nImplementation example completed!")

if __name__ == "__main__":
    main() 