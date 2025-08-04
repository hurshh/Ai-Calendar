# AI Calendar Web Application

A modern, intelligent calendar management system that combines Google Calendar with natural language processing.

## Features

- **Natural Language Interface**: Chat with the AI to manage your calendar
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Real-time Updates**: Calendar view updates automatically when changes are made
- **Smart Scheduling**: AI understands complex scheduling requests
- **Availability Checking**: Find free time slots easily

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   - Create `.env` file in config directory
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your-key-here
     ```

3. Set up Google Calendar:
   - Follow instructions in CHATBOT_SETUP.md
   - Place credentials.json in config directory

4. Run the application:
   ```bash
   python scripts/run_web_app.py
   ```

5. Access the web interface:
   - Open http://localhost:5001 in your browser
   - Start chatting with the AI to manage your calendar!

## Mobile Experience

The web interface is fully responsive and works great on mobile devices:
- Clean, touch-friendly interface
- Easy-to-read calendar view
- Smooth chat interaction
- Automatic event refresh 