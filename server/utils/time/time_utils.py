"""
Time utility functions
"""

from datetime import datetime
import pytz

def format_events_for_display(events):
    """Format events for frontend display"""
    formatted_events = []
    for event in events:
        try:
            start = event.get('start', {}).get('dateTime', '')
            end = event.get('end', {}).get('dateTime', '')
            
            # Convert to local time for display
            if start:
                start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                local_start = start_dt.astimezone(pytz.timezone('Asia/Kolkata'))
                start_formatted = local_start.strftime('%Y-%m-%d %H:%M')
            else:
                start_formatted = 'Unknown'
            
            if end:
                end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
                local_end = end_dt.astimezone(pytz.timezone('Asia/Kolkata'))
                end_formatted = local_end.strftime('%H:%M')
            else:
                end_formatted = 'Unknown'
            
            formatted_events.append({
                'id': event.get('id', ''),
                'title': event.get('summary', 'Untitled Event'),
                'start': start_formatted,
                'end': end_formatted,
                'description': event.get('description', ''),
                'location': event.get('location', ''),
                'day': local_start.strftime('%A, %B %d') if start else 'Unknown'
            })
        except Exception as e:
            print(f"Error formatting event: {e}")
            continue
    
    return formatted_events

def parse_datetime(date_str: str, timezone=None) -> datetime:
    """Parse datetime string to datetime object"""
    dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    if timezone:
        dt = dt.astimezone(timezone)
    return dt

def format_datetime(dt: datetime, format_str: str = '%Y-%m-%dT%H:%M:%S.000Z') -> str:
    """Format datetime object to string"""
    return dt.strftime(format_str) 