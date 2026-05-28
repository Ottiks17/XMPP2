# XMPP2 — XMPP Messaging Client with REST API

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Release](https://img.shields.io/badge/release-v1.0.1-brightgreen.svg)](https://github.com/Ottiks17/XMPP2/releases)

Professional XMPP (Jabber) client for Windows with built-in REST API server for system integrations.

## ✨ Features

- **XMPP Connectivity** — TLS encryption, optional certificate verification, in-band registration
- **Modern GUI** — PyQt5 interface with chat history, delivery statuses, and read receipts
- **REST API** — Flask + Waitress server for external system integration
- **Persistence** — SQLite logging, JSON export, automatic log cleanup
- **Security First** — API key authentication, environment variables for secrets, config priority system
- **Auto-Updates** — Built-in update checker with download prompts

## 🚀 Quick Start

### Prerequisites
- Windows 10/11
- Python 3.10 or higher
- Git (optional, for cloning)

### One-Click Launch
\\\at
run.bat
\\\

### Manual Setup
\\\powershell
# Clone the repository
git clone https://github.com/Ottiks17/XMPP2.git
cd XMPP2

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
\\\

## ⚙️ Configuration

### Required: XMPP Account
1. Copy \config/config.example.json\ → \config/config.json\
2. Fill in your XMPP server credentials

### Optional: Environment Variables
Create \.env\ file (see \.env.example\):
\\\env
XMPP_PASSWORD=your-secure-password
REST_API_KEY=your-long-random-api-key
\\\

**Priority order:** \.env\ → \config.json\ → built-in defaults

## 🌐 REST API

Starts on \http://127.0.0.1:8080\ by default.

| Method | Endpoint | Auth Required | Description |
|--------|----------|:---:|-------------|
| \POST\ | \/send_message\ | API Key | Send message to user |
| \POST\ | \/broadcast\ | API Key | Send to multiple recipients |
| \GET\ | \/health\ | No | Health check |
| \GET\ | \/stats\ | API Key | Message statistics |
| \GET\ | \/get_messages\ | API Key | Message history |
| \GET\ | \/apidocs\ | No | API documentation |

### Example
\\\powershell
curl -X POST http://127.0.0.1:8080/send_message \
  -H \"Content-Type: application/json\" \
  -H \"X-API-Key: your-api-key\" \
  -d '{\"to\": \"friend@example.com\", \"message\": \"Hello from API!\"}'
\\\

> ⚠️ GET method for sending is disabled by default (\llow_get: false\)

## 🏗️ Architecture

\\\
┌─────────────────┐     ┌──────────────────┐     ┌─────────────┐
│   gui_app.py    │────▶│ app/xmpp/        │────▶│  XMPP       │
│   (PyQt5 GUI)   │◀────│ service.py       │◀────│  Server     │
└─────────────────┘     │ (slixmpp client) │     └─────────────┘
                        └────────┬─────────┘
                                 │
┌─────────────────┐              │
│  rest_server.py │──────────────┘
│  (Flask +       │
│   Waitress)     │
└─────────────────┘
\\\

## 📁 Project Structure

\\\
├── app/
│   ├── config.py        # Configuration loader
│   ├── storage.py       # SQLite logger
│   ├── validation.py    # JID & message validation
│   └── xmpp/
│       └── service.py   # slixmpp client implementation
├── tools/               # Utility scripts
│   ├── build.bat        # Build script
│   ├── fixG.py          # GUI patcher
│   ├── fixH.py          # Update mechanism patcher
│   ├── view_db.py       # Database viewer
│   └── view_logs.py     # Log viewer
├── tests/               # Automated tests
├── config/
│   └── config.example.json
├── logs/                # Application logs (gitignored)
├── gui_app.py           # PyQt5 interface
├── rest_server.py       # REST API server
├── main.py              # Entry point
├── requirements.txt     # Dependencies
└── README.md
\\\

## 🧪 Development

### Running Tests
\\\powershell
venv\Scripts\activate
pytest -q
\\\

### Code Quality
\\\powershell
# Install dev dependencies
pip install black isort flake8

# Format code
black .
isort .

# Lint
flake8 .
\\\

## 🔒 Security Best Practices

- ✅ Use \pi_key\ when exposing API to network
- ✅ Never commit \config.json\ (gitignored)
- ✅ Store passwords only in \.env\ file
- ✅ Set \erify_tls: true\ for production with valid certificates
- ✅ Use strong random API keys (e.g., \python -c "import secrets; print(secrets.token_urlsafe(32))"\)

## 📝 Logs

- \logs/app.log\ — Text logs
- \logs/messages.db\ — SQLite database
- \logs/chat_history.json\ — GUI chat history

## 👤 Author

**Vladislav (Ottiks17)**

- GitHub: [@Ottiks17](https://github.com/Ottiks17)
- Project: [XMPP2](https://github.com/Ottiks17/XMPP2)
- Contact: [Open an issue](https://github.com/Ottiks17/XMPP2/issues) for questions or suggestions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (\git checkout -b feature/amazing-feature\)
3. Make atomic, well-described commits
4. Add tests for new functionality
5. Submit a Pull Request

## 📄 License

MIT License — see [LICENSE](LICENSE) file for details.

---

**Made with ❤️ for the XMPP community**
