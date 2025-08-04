"""
Web application API endpoints
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from services.chatbot.calendar_chatbot_gpt import CalendarGPTBot
from services.calendar.calendar_handler import CalendarHandler
from datetime import datetime, timedelta
import pytz
import os
from config.settings import (
    OPENAI_API_KEY,
    DEBUG,
    HOST,
    PORT,
    GOOGLE_CREDENTIALS_FILE,
    GOOGLE_TOKEN_FILE
)

# Initialize Flask app with correct template directory
app = Flask(__name__, static_folder='../static')
CORS(app)

# Initialize the chatbot and calendar handler
if not OPENAI_API_KEY:
    print("Warning: OPENAI_API_KEY not found. Chat functionality will be limited.")
    chatbot = None
else:
    try:
        chatbot = CalendarGPTBot(OPENAI_API_KEY)
    except Exception as e:
        print(f"Error initializing chatbot: {e}")
        chatbot = None

# Initialize calendar handler for direct calendar access
calendar_handler = CalendarHandler()
try:
    calendar_handler.authenticate()
except Exception as e:
    print(f"Error authenticating calendar: {e}")
    calendar_handler = None

@app.route('/')
def index():
    """Serve the main calendar interface"""
    return app.send_static_file('index.html')

@app.route('/api/events')
def get_events():
    """Get calendar events for display"""
    try:
        if not calendar_handler:
            return jsonify({'error': 'Calendar not available'}), 500
        
        # Get events for the next 7 days by default
        start_date = datetime.now(pytz.UTC)
        end_date = start_date + timedelta(days=7)
        
        start_time = start_date.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        end_time = end_date.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        
        events = calendar_handler.get_events(start_time=start_time, end_time=end_time)
        
        # Format events for frontend
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
        
        return jsonify({'events': formatted_events})
        
    except Exception as e:
        print(f"Error getting events: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        if not chatbot:
            return jsonify({'error': 'Chatbot not available. Please check OpenAI API key.'}), 500
        
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Process the message with the chatbot
        response = chatbot.process_query(message)
        
        return jsonify({'response': response})
        
    except Exception as e:
        print(f"Error in chat: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/refresh')
def refresh_events():
    """Refresh calendar events"""
    return get_events()

if __name__ == '__main__':
    print("Starting Calendar Web App...")
    print("Make sure your OpenAI API key is set in the .env file")
    print("Access the app at: http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001) 