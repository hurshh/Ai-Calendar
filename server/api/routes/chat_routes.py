"""
Chat API routes
"""

from flask import Blueprint, jsonify, request
from api.controllers.chat_controller import ChatController

chat_routes = Blueprint('chat_routes', __name__)
controller = ChatController()

@chat_routes.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    return controller.process_message() 