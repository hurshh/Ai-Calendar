# 🗓️ AI Calendar Web Application

A beautiful, modern web interface for managing your Google Calendar with AI-powered chat assistance.

## ✨ Features

- **📅 Calendar Display**: View your upcoming events in a clean, organized layout
- **💬 AI Chat Assistant**: Natural language interaction for calendar management
- **📱 Responsive Design**: Works perfectly on desktop and mobile devices
- **🔄 Real-time Updates**: Calendar refreshes automatically after scheduling events
- **🌟 Modern UI**: Beautiful gradient background with glass-morphism effects

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd server
pip install -r requirements.txt
```

### 2. Set up Environment Variables
Create a `.env` file in the server directory:
```
OPENAI_API_KEY=your-openai-api-key-here
```

Get your OpenAI API key from: https://platform.openai.com/api-keys

### 3. Set up Google Calendar (Optional)
- Follow the instructions in `CHATBOT_SETUP.md`
- Place your `credentials.json` file in the server directory

### 4. Run the Application
```bash
python run_web_app.py
```

Or directly:
```bash
python web_app.py
```

### 5. Access the App
Open your browser and go to: **http://localhost:5000**

## 🎯 How to Use

### Calendar View (Left Side)
- **View Events**: See your upcoming events organized by day
- **Refresh Button**: Manually refresh the calendar display
- **Event Details**: Each event shows:
  - 📝 Title
  - 🕐 Time (start - end)
  - 📍 Location (if available)
  - 📄 Description (if available)

### Chat Assistant (Right Side)
The AI assistant can help you with:

#### 📅 Viewing Events
- "What's on my calendar today?"
- "Show me tomorrow's meetings"
- "What events do I have this week?"

#### ➕ Scheduling Events
- "Schedule a team meeting tomorrow at 2 PM for 1 hour"
- "Create a dentist appointment on 2024-01-25 at 10:00 for 30 minutes"
- "Add a lunch meeting at 12:30 PM tomorrow"

#### 🔍 Finding Available Times
- "When am I free tomorrow?"
- "Find me a 30-minute slot for tomorrow"
- "What time slots are available next Monday?"

#### ✏️ Updating Events
- "Update event abc123 title to 'Updated Meeting'"
- "Change the time of event xyz789 to tomorrow at 3 PM"

#### 🗑️ Deleting Events
- "Delete event abc123"
- "Cancel the meeting with ID xyz789"

## 🛠️ Technical Details

### Backend (`web_app.py`)
- **Framework**: Flask with CORS support
- **APIs**:
  - `GET /` - Serve the web interface
  - `GET /api/events` - Fetch calendar events
  - `POST /api/chat` - Process chat messages
  - `GET /api/refresh` - Refresh calendar events

### Frontend (`templates/index.html`)
- **Responsive Design**: CSS Grid and Flexbox
- **Modern Styling**: Gradient backgrounds, glass-morphism effects
- **JavaScript**: Async/await for API calls, real-time chat interface
- **Mobile-First**: Responsive layout that works on all screen sizes

### Integration
- **Google Calendar**: Direct integration via `calendar_handler.py`
- **OpenAI GPT**: Natural language processing via `calendar_chatbot_gpt.py`
- **Future Events Filter**: Shows only upcoming events by default

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Required for chat functionality
- Add to `.env` file in the server directory

### Google Calendar Setup
1. Create a project in Google Cloud Console
2. Enable Google Calendar API
3. Create credentials (OAuth 2.0)
4. Download `credentials.json`
5. Place in server directory

### Port Configuration
Default port is 5000. To change:
```python
app.run(debug=True, host='0.0.0.0', port=YOUR_PORT)
```

## 🎨 Customization

### Styling
All styles are in the `<style>` section of `templates/index.html`:
- **Colors**: Modify the gradient background and accent colors
- **Layout**: Adjust flex ratios for calendar vs chat sections
- **Typography**: Change fonts in the CSS

### Features
- **Time Zone**: Currently set to 'Asia/Kolkata' in `web_app.py`
- **Event Range**: Shows next 7 days by default
- **Chat History**: Persists during session

## 🐛 Troubleshooting

### Common Issues

1. **"Flask not found"**
   ```bash
   pip install -r requirements.txt
   ```

2. **"OpenAI API key missing"**
   - Create `.env` file with `OPENAI_API_KEY=your-key`
   - Get key from: https://platform.openai.com/api-keys

3. **"Calendar not available"**
   - Follow Google Calendar setup in `CHATBOT_SETUP.md`
   - Ensure `credentials.json` is in server directory

4. **"No events found"**
   - Check your Google Calendar has events
   - Verify date ranges in the application

### Debug Mode
The app runs in debug mode by default, showing detailed error messages in the console.

## 📱 Mobile Experience

The web app is fully responsive:
- **Mobile Layout**: Stacked sections (calendar above, chat below)
- **Touch-Friendly**: Large buttons and input areas
- **Responsive Text**: Scales appropriately for mobile screens

## 🚀 Deployment

For production deployment:
1. Set `debug=False` in `web_app.py`
2. Use a production WSGI server like Gunicorn
3. Set up proper environment variable management
4. Configure HTTPS and security headers

## 🤝 Contributing

Feel free to contribute improvements:
- UI/UX enhancements
- Additional calendar features
- Mobile app version
- Better error handling

---

**Made with ❤️ using Flask, OpenAI GPT, and Google Calendar API** 