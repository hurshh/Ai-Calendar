"""
Calendar API routes
"""

from flask import Blueprint, jsonify, request
from api.controllers.calendar_controller import CalendarController
from utils.time.time_utils import format_events_for_display

calendar_routes = Blueprint('calendar_routes', __name__)
controller = CalendarController()

@calendar_routes.route('/events')
def get_events():
    """Get calendar events for display"""
    return controller.get_events()

@calendar_routes.route('/refresh')
def refresh_events():
    """Refresh calendar events"""
    return controller.get_events() 