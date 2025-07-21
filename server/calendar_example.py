#!/usr/bin/env python3
"""
Example usage of the CalendarHandler

This script demonstrates how to use the CalendarHandler for:
- Authentication
- Adding events
- Deleting events
- Checking availability
- Finding available slots
"""

from calendar_handler import CalendarHandler
from datetime import datetime, timedelta

def main():
    """
    Demonstrate CalendarHandler functionality
    """
    print("Calendar Handler Demo")
    print("="*50)
    
    # Create handler instance
    handler = CalendarHandler()
    
    # Step 1: Authenticate
    print("\nStep 1: Authentication")
    if not handler.authenticate():
        print("Authentication failed. Exiting.")
        return
    
    # Step 2: Get calendars
    print("\nStep 2: Get Calendars")
    calendars = handler.get_calendars()
    print(f"Found {len(calendars)} calendars:")
    for i, cal in enumerate(calendars[:3]):
        primary_marker = " (Primary)" if cal.get('primary') else ""
        print(f"  {i+1}. {cal['summary']}{primary_marker}")
    
    # Step 3: Check availability
    print("\nStep 3: Check Availability")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    start_time = f"{tomorrow}T10:00:00"
    end_time = f"{tomorrow}T11:00:00"
    
    is_available, conflicts = handler.check_availability(start_time, end_time)
    if is_available:
        print(f"Time slot {start_time} to {end_time} is available")
    else:
        print(f"Time slot {start_time} to {end_time} has conflicts:")
        for conflict in conflicts[:3]:
            print(f"  - {conflict.get('summary', 'No title')}")
    
    # Step 4: Find available slots
    print("\nStep 4: Find Available Slots")
    available_slots = handler.find_available_slots(
        date=tomorrow,
        duration_minutes=60,
        start_hour=9,
        end_hour=17
    )
    
    print(f"Available 1-hour slots on {tomorrow}:")
    for i, slot in enumerate(available_slots[:5]):
        start_dt = datetime.fromisoformat(slot['start_time'])
        end_dt = datetime.fromisoformat(slot['end_time'])
        print(f"  {i+1}. {start_dt.strftime('%I:%M %p')} - {end_dt.strftime('%I:%M %p')}")
    
    if len(available_slots) > 5:
        print(f"  ... and {len(available_slots) - 5} more")
    
    # Step 5: Add an event (if we have available slots)
    print("\nStep 5: Add Event")
    if available_slots:
        # Use the first available slot
        slot = available_slots[0]
        event_id = handler.add_event(
            title="Demo Meeting",
            start_time=slot['start_time'],
            duration_minutes=60,
            description="This is a demo meeting created by CalendarHandler",
            location="Virtual Meeting",
            attendees=["demo@example.com"]
        )
        
        if event_id:
            print(f"Event created successfully with ID: {event_id}")
            
            # Step 6: Get event details
            print("\nStep 6: Get Event Details")
            event = handler.get_event(event_id)
            if event:
                print(f"Event: {event.get('summary')}")
                print(f"Start: {event.get('start')}")
                print(f"End: {event.get('end')}")
                print(f"Description: {event.get('description')}")
            
            # Step 7: Update event
            print("\nStep 7: Update Event")
            success = handler.update_event(
                event_id=event_id,
                title="Updated Demo Meeting",
                description="This meeting has been updated"
            )
            if success:
                print("Event updated successfully")
            
            # Step 8: Delete event
            print("\nStep 8: Delete Event")
            success = handler.delete_event(event_id)
            if success:
                print("Event deleted successfully")
        else:
            print("Failed to create event")
    else:
        print("No available slots found for creating a test event")
    
    # Step 9: Get events for next week
    print("\nStep 9: Get Events for Next Week")
    next_week_start = datetime.now().isoformat()
    next_week_end = (datetime.now() + timedelta(days=7)).isoformat()
    
    events = handler.get_events(
        start_time=next_week_start,
        end_time=next_week_end,
        max_results=10
    )
    
    print(f"Events in the next week:")
    for i, event in enumerate(events[:5]):
        title = event.get('summary', 'No title')
        start = event.get('start', {}).get('dateTime', 'All day')
        if 'T' in start:
            start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
            time_str = start_dt.strftime("%I:%M %p")
        else:
            time_str = "All Day"
        print(f"  {i+1}. {title} - {time_str}")
    
    if len(events) > 5:
        print(f"  ... and {len(events) - 5} more")
    
    print("\nDemo completed successfully!")

if __name__ == "__main__":
    main() 