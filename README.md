# AI Crypto Monitor

AI-powered cryptocurrency monitoring and analysis tool that fetches real-time prices, generates market insights using AI, and logs data to Google Sheets.

## Features

- 📊 Real-time BTC & ETH price fetching from CoinGecko
- 🧠 AI-powered market sentiment analysis using OpenAI
- 📝 Automated logging to Google Sheets
- 📈 Weekly trend reports and analysis
- 🏗️ Clean, modular architecture with `src/` layout

## Project Structure

```
ai-crypto-monitor/
├── src/
│   └── crypto_monitor/          # Main package
│       ├── __init__.py          # Package initialization
│       ├── api/                 # External API clients
│       │   ├── __init__.py
│       │   └── coingecko.py    # CoinGecko price fetching
│       ├── agents/              # AI analysis agents
│       │   ├── __init__.py
│       │   ├── daily_agent.py  # Daily market analysis
│       │   └── weekly_agent.py # Weekly trend reports
│       ├── storage/             # Data persistence
│       │   ├── __init__.py
│       │   └── sheets_logger.py # Google Sheets logging
│       ├── models/              # Data models
│       │   ├── __init__.py
│       │   └── schemas.py      # Pydantic models
│       └── utils/               # Utilities
│           ├── __init__.py
│           └── config.py       # Configuration management
├── scripts/                     # Entry point scripts
│   ├── daily_run.py            # Daily monitoring script
│   └── weekly_report.py        # Weekly analysis script
├── .env                         # Environment variables (not in git)
├── crypto_creds.json           # Google service account (not in git)
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
SHEET_ID=your_google_sheet_id_here
```

### 3. Set Up Google Sheets Credentials

- Create a Google Cloud project and enable the Google Sheets API
- Create a service account and download the credentials JSON
- Save as `crypto_creds.json` in the project root
- Share your Google Sheet with the service account email

## Usage

### Daily Price Monitoring

Fetch current crypto prices and generate AI analysis:

```bash
python scripts/daily_run.py
```

This will:
- Fetch current BTC and ETH prices from CoinGecko
- Generate AI sentiment analysis
- Log results to Google Sheets

### Weekly Trend Report

Generate a weekly analysis report:

```bash
python scripts/weekly_report.py
```

This will:
- Analyze the last 7 days of logged data
- Generate a weekly summary with AI
- Save the report to the Weekly_Reports sheet

### Using as a Python Package

You can also import and use the modules directly:

```python
import sys
sys.path.insert(0, 'src')

from crypto_monitor.api import fetch_crypto_prices
from crypto_monitor.agents import summarize_crypto
from crypto_monitor.storage import log_crypto_data

# Fetch prices
btc, eth = fetch_crypto_prices()
print(f"BTC: ${btc}, ETH: ${eth}")

# Analyze
result = summarize_crypto(f"Bitcoin is ${btc} and Ethereum is ${eth}")
print(result.sentiment)

# Log to Google Sheets
log_crypto_data(btc, eth, result.summary, result.sentiment, result.reasoning)
```

## Architecture Benefits

The `src/` directory structure provides:

1. **Clean Separation**: Clear boundaries between API, AI, storage, and models
2. **Easy Testing**: Each module can be tested independently
3. **Scalability**: Easy to add new cryptocurrencies, data sources, or analysis types
4. **Professional**: Follows Python packaging best practices
5. **Maintainability**: Related code is grouped together logically

## Adding New Features

### Adding a New Cryptocurrency

Edit `src/crypto_monitor/api/coingecko.py` to include more coins in the API request.

### Adding New Analysis

Create a new agent in `src/crypto_monitor/agents/` following the pattern of `daily_agent.py`.

### Adding New Data Destinations

Create a new logger in `src/crypto_monitor/storage/` (e.g., `database_logger.py`, `slack_notifier.py`).

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest

# Run tests
pytest tests/
```

### Code Quality

```bash
# Format code
black src/

# Type checking
mypy src/

# Linting
pylint src/
```

## License

MIT

## Author

zautt
