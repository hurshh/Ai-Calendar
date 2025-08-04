"""
Main application entry point for the AI Calendar Server
"""

from api import create_app
from config.settings import HOST, PORT, DEBUG

def main():
    """Run the application"""
    app = create_app()
    print("Starting AI Calendar Server...")
    print(f"Access the app at: http://{HOST}:{PORT}")
    app.run(debug=DEBUG, host=HOST, port=PORT)

if __name__ == "__main__":
    main() 