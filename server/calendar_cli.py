#!/usr/bin/env python3

import argparse
from datetime import datetime, timedelta
from calendar_handler import CalendarHandler

def format_time(date_str, time_str=None):
    """Convert date and optional time to ISO format."""
    if time_str:
        dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    else:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
    return dt.isoformat()

def list_events(handler, args):
    """List events within a date range."""
    start_time = format_time(args.start_date, "00:00") if args.start_date else None
    end_time = format_time(args.end_date, "23:59") if args.end_date else None
    
    events = handler.get_events(start_time=start_time, end_time=end_time, max_results=args.max_results)
    
    if not events:
        print("No events found.")
        return
    
    print("\nUpcoming events:")
    for event in events:
        start = event.get('start', {}).get('dateTime', event.get('start', {}).get('date'))
        print(f"- {event.get('summary')} (ID: {event.get('id')})")
        print(f"  Start: {start}")
        print()

def add_event(handler, args):
    """Add a new calendar event."""
    start_time = format_time(args.date, args.time)
    
    attendees = args.attendees.split(',') if args.attendees else None
    
    event_id = handler.add_event(
        title=args.title,
        start_time=start_time,
        duration_minutes=args.duration,
        description=args.description,
        location=args.location,
        attendees=attendees
    )
    
    if event_id:
        print(f"Event created successfully! Event ID: {event_id}")
    else:
        print("Failed to create event.")

def delete_event(handler, args):
    """Delete a calendar event."""
    if handler.delete_event(args.event_id):
        print("Event deleted successfully!")
    else:
        print("Failed to delete event.")

def main():
    parser = argparse.ArgumentParser(description="Google Calendar Command Line Interface")
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # List events command
    list_parser = subparsers.add_parser('list', help='List calendar events')
    list_parser.add_argument('--start-date', help='Start date (YYYY-MM-DD)')
    list_parser.add_argument('--end-date', help='End date (YYYY-MM-DD)')
    list_parser.add_argument('--max-results', type=int, default=10, help='Maximum number of events to return')
    
    # Add event command
    add_parser = subparsers.add_parser('add', help='Add a new event')
    add_parser.add_argument('--title', required=True, help='Event title')
    add_parser.add_argument('--date', required=True, help='Event date (YYYY-MM-DD)')
    add_parser.add_argument('--time', required=True, help='Event time (HH:MM)')
    add_parser.add_argument('--duration', type=int, default=60, help='Event duration in minutes')
    add_parser.add_argument('--description', default='', help='Event description')
    add_parser.add_argument('--location', default='', help='Event location')
    add_parser.add_argument('--attendees', help='Comma-separated list of attendee emails')
    
    # Delete event command
    delete_parser = subparsers.add_parser('delete', help='Delete an event')
    delete_parser.add_argument('event_id', help='Event ID to delete')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize and authenticate calendar handler
    handler = CalendarHandler()
    if not handler.authenticate():
        print("Failed to authenticate with Google Calendar.")
        return
    
    # Execute the appropriate command
    if args.command == 'list':
        list_events(handler, args)
    elif args.command == 'add':
        add_event(handler, args)
    elif args.command == 'delete':
        delete_event(handler, args)

if __name__ == '__main__':
    main() 