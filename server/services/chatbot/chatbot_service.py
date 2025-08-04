"""
Chatbot service handling chat operations
"""

from services.chatbot.calendar_chatbot_gpt import CalendarGPTBot
from config.settings import OPENAI_API_KEY

class ChatbotService:
    def __init__(self):
        """Initialize chatbot service"""
        try:
            if OPENAI_API_KEY:
                self.bot = CalendarGPTBot(OPENAI_API_KEY)
            else:
                print("Warning: OPENAI_API_KEY not found. Chat functionality will be limited.")
                self.bot = None
        except Exception as e:
            print(f"Error initializing chatbot: {e}")
            self.bot = None

    def is_available(self) -> bool:
        """Check if chatbot service is available"""
        return self.bot is not None

    def process_message(self, message: str) -> str:
        """Process a chat message"""
        return self.bot.process_query(message) 