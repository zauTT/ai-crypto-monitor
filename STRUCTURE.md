# Project Structure Explained

## Understanding `__init__.py` Files

This document explains what each `__init__.py` file does in the project.

### Root Package: `src/crypto_monitor/__init__.py`

```python
# What it does:
# 1. Loads .env variables when package is imported
# 2. Defines package version
# 3. Makes "crypto_monitor" a proper Python package

from dotenv import load_dotenv
load_dotenv()  # Runs automatically on: import crypto_monitor

__version__ = "0.1.0"
```

**When imported:**
```python
import crypto_monitor
print(crypto_monitor.__version__)  # "0.1.0"
# .env is now loaded automatically!
```

---

### API Package: `src/crypto_monitor/api/__init__.py`

```python
# What it does:
# Re-exports fetch_crypto_prices for easier imports

from .coingecko import fetch_crypto_prices
__all__ = ['fetch_crypto_prices']
```

**Without this file:**
```python
from crypto_monitor.api.coingecko import fetch_crypto_prices  # Long!
```

**With this file:**
```python
from crypto_monitor.api import fetch_crypto_prices  # Clean!
```

---

### Agents Package: `src/crypto_monitor/agents/__init__.py`

```python
# What it does:
# Re-exports both AI agent functions

from .daily_agent import summarize_crypto
from .weekly_agent import analyze_week
__all__ = ['summarize_crypto', 'analyze_week']
```

**Usage:**
```python
from crypto_monitor.agents import summarize_crypto, analyze_week
# Instead of importing from daily_agent and weekly_agent separately
```

---

### Storage Package: `src/crypto_monitor/storage/__init__.py`

```python
# What it does:
# Re-exports storage functions

from .sheets_logger import log_crypto_data, get_gspread_client
__all__ = ['log_crypto_data', 'get_gspread_client']
```

**Usage:**
```python
from crypto_monitor.storage import log_crypto_data
# Instead of: from crypto_monitor.storage.sheets_logger import log_crypto_data
```

---

### Models Package: `src/crypto_monitor/models/__init__.py`

```python
# What it does:
# Re-exports Pydantic models

from .schemas import CryptoSummary, WeeklyInsight
__all__ = ['CryptoSummary', 'WeeklyInsight']
```

**Usage:**
```python
from crypto_monitor.models import CryptoSummary, WeeklyInsight
result = CryptoSummary(summary="...", sentiment="Bullish", reasoning="...")
```

---

### Utils Package: `src/crypto_monitor/utils/__init__.py`

```python
# What it does:
# Re-exports configuration getter

from .config import get_config
__all__ = ['get_config']
```

**Usage:**
```python
from crypto_monitor.utils import get_config
config = get_config()
print(config.sheet_id)
```

---

## Directory Structure Visualization

```
ai-crypto-monitor/
│
├── src/crypto_monitor/          # Main package (importable)
│   ├── __init__.py             # Loads .env, defines version
│   │                           # Makes crypto_monitor importable
│   │
│   ├── api/                    # External API clients
│   │   ├── __init__.py        # Exports: fetch_crypto_prices
│   │   └── coingecko.py       # Implementation: CoinGecko API
│   │
│   ├── agents/                 # AI analysis
│   │   ├── __init__.py        # Exports: summarize_crypto, analyze_week
│   │   ├── daily_agent.py     # Implementation: Daily AI analysis
│   │   └── weekly_agent.py    # Implementation: Weekly AI analysis
│   │
│   ├── storage/                # Data persistence
│   │   ├── __init__.py        # Exports: log_crypto_data, get_gspread_client
│   │   └── sheets_logger.py   # Implementation: Google Sheets logging
│   │
│   ├── models/                 # Data models
│   │   ├── __init__.py        # Exports: CryptoSummary, WeeklyInsight
│   │   └── schemas.py         # Implementation: Pydantic models
│   │
│   └── utils/                  # Utilities
│       ├── __init__.py        # Exports: get_config
│       └── config.py          # Implementation: Configuration class
│
├── scripts/                    # Entry points (not importable as package)
│   ├── daily_run.py           # Run: python scripts/daily_run.py
│   └── weekly_report.py       # Run: python scripts/weekly_report.py
│
├── tests/                      # Unit tests
│   └── (future test files)
│
├── .env                        # Environment variables
├── crypto_creds.json          # Google credentials
├── requirements.txt           # Dependencies
└── README.md                  # Documentation
```

## Import Flow Example

When you run `scripts/daily_run.py`:

```python
# Step 1: Add src to path
import sys
sys.path.insert(0, 'src')

# Step 2: Import from crypto_monitor
from crypto_monitor.api import fetch_crypto_prices
# This triggers:
#   1. crypto_monitor/__init__.py (loads .env)
#   2. crypto_monitor/api/__init__.py (imports from coingecko.py)

# Step 3: Use the function
btc, eth = fetch_crypto_prices()
```

## Benefits of This Structure

1. **Clean Imports**: Short, readable import statements
2. **Separation of Concerns**: Each directory has a specific purpose
3. **Easy Testing**: Can import and test individual modules
4. **Scalability**: Easy to add new API clients, agents, or storage backends
5. **Professional**: Follows Python packaging best practices
6. **Documentation**: Clear structure makes code self-documenting

## Adding New Features

### Adding a New Cryptocurrency API

1. Create `src/crypto_monitor/api/binance.py`
2. Add function: `def fetch_binance_prices(): ...`
3. Export in `src/crypto_monitor/api/__init__.py`:
   ```python
   from .binance import fetch_binance_prices
   __all__ = ['fetch_crypto_prices', 'fetch_binance_prices']
   ```

### Adding a New Storage Backend

1. Create `src/crypto_monitor/storage/database_logger.py`
2. Add function: `def log_to_postgres(...): ...`
3. Export in `src/crypto_monitor/storage/__init__.py`:
   ```python
   from .database_logger import log_to_postgres
   __all__ = ['log_crypto_data', 'get_gspread_client', 'log_to_postgres']
   ```

### Adding Tests

1. Create `tests/test_api.py`:
   ```python
   import sys
   sys.path.insert(0, 'src')

   from crypto_monitor.api import fetch_crypto_prices

   def test_fetch_prices():
       btc, eth = fetch_crypto_prices()
       assert btc > 0
       assert eth > 0
   ```

2. Run: `pytest tests/`

---

**Questions?** Check the main README.md or examine the `__init__.py` files directly!
