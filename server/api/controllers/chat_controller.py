"""
Chat controller handling chat operations
"""

from flask import jsonify, request
from services.chatbot.chatbot_service import ChatbotService

class ChatController:
    def __init__(self):
        """Initialize chat controller"""
        self.service = ChatbotService()

    def process_message(self):
        """Process chat messages"""
        try:
            if not self.service.is_available():
                return jsonify({'error': 'Chatbot not available. Please check OpenAI API key.'}), 500
            
            data = request.get_json()
            message = data.get('message', '').strip()
            
            if not message:
                return jsonify({'error': 'Message cannot be empty'}), 400
            
            # Process the message with the chatbot
            response = self.service.process_message(message)
            
            return jsonify({'response': response})
            
        except Exception as e:
            print(f"Error in chat: {e}")
            return jsonify({'error': str(e)}), 500 