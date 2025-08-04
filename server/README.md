# AI Calendar Server

Backend server for the AI Calendar application with GPT-powered chat interface.

## 📁 Directory Structure

```
server/
├── api/                    # API Layer
│   ├── routes/            # URL routing
│   │   ├── calendar_routes.py
│   │   └── chat_routes.py
│   ├── controllers/       # Request handling
│   │   ├── calendar_controller.py
│   │   └── chat_controller.py
│   └── middleware/        # Request/response middleware
│
├── services/              # Business Logic
│   ├── calendar/         # Calendar operations
│   │   ├── calendar_handler.py
│   │   └── calendar_service.py
│   └── chatbot/          # Chat operations
│       ├── calendar_chatbot_gpt.py
│       └── chatbot_service.py
│
├── models/               # Data models
│   ├── calendar/        # Calendar-related models
│   └── chat/           # Chat-related models
│
├── utils/               # Utility functions
│   ├── time/           # Time handling utilities
│   │   └── time_utils.py
│   └── validators/     # Input validation
│
├── config/             # Configuration
│   ├── settings.py     # Application settings
│   ├── .env           # Environment variables
│   └── credentials/    # API credentials
│
├── static/             # Static files
│   └── index.html     # Web interface
│
├── tests/              # Test files
│   ├── unit/          # Unit tests
│   └── integration/   # Integration tests
│
├── scripts/           # Utility scripts
│   └── old/          # Legacy code for reference
│
└── docs/             # Documentation
    ├── CHATBOT_SETUP.md
    ├── WEB_APP_README.md
    └── calendar_handler.md
```

## 🚀 Quick Start

1. **Set up environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure credentials**:
- Copy `.env.example` to `.env` and set your OpenAI API key
- Follow `docs/CHATBOT_SETUP.md` for Google Calendar setup
- Place credentials in `config/credentials/`

3. **Run the server**:
```bash
python app.py
```

## 🔧 Development

### Running Tests
```bash
# Run unit tests
python -m pytest tests/unit

# Run integration tests
python -m pytest tests/integration
```

### Code Style
- Black for formatting
- Flake8 for linting
- MyPy for type checking

### Adding New Features
1. Add routes in `api/routes/`
2. Create controllers in `api/controllers/`
3. Implement business logic in `services/`
4. Add models if needed in `models/`
5. Add tests in `tests/`

## 📚 Documentation

- [Chatbot Setup](docs/CHATBOT_SETUP.md)
- [Web App Guide](docs/WEB_APP_README.md)
- [Calendar Handler](docs/calendar_handler.md)

## 🔒 Security

- Store sensitive data in `.env`
- Keep credentials in `config/credentials/`
- Never commit sensitive files (check `.gitignore`)

## 🐛 Troubleshooting

Common issues:
1. **"Module not found"**: Check virtual environment and requirements
2. **"Credentials not found"**: Check `config/credentials/`
3. **"API key invalid"**: Verify `.env` configuration

## 📦 Dependencies

See `requirements.txt` for full list:
- Flask for web server
- OpenAI for chat
- Google Calendar API
- PyTest for testing 