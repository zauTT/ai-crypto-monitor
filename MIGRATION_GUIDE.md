# Migration Guide: Old Files → New Structure

This guide shows how the old files map to the new `src/` structure.

## Quick Reference

| Old File | New Location | Purpose |
|----------|--------------|---------|
| `main.py` | `scripts/daily_run.py` | Daily monitoring entry point |
| `crypto_agent.py` | `src/crypto_monitor/agents/daily_agent.py` | Daily AI analysis |
| `crypto_logger.py` | `src/crypto_monitor/storage/sheets_logger.py` | Google Sheets logging |
| `trend_analyzer.py` | `src/crypto_monitor/agents/weekly_agent.py` | Weekly trend analysis |
| N/A | `src/crypto_monitor/api/coingecko.py` | API client (extracted) |
| N/A | `src/crypto_monitor/models/schemas.py` | Pydantic models (extracted) |
| N/A | `src/crypto_monitor/utils/config.py` | Configuration (new) |

## Detailed Changes

### 1. `main.py` → `scripts/daily_run.py`

**Old:**
```python
# main.py (in project root)
from crypto_agent import summarize_crypto
from crypto_logger import log_crypto_data

def fetch_crypto_prices():
    # ... API call here ...
```

**New:**
```python
# scripts/daily_run.py
import sys
sys.path.insert(0, 'src')

from crypto_monitor.api import fetch_crypto_prices
from crypto_monitor.agents import summarize_crypto
from crypto_monitor.storage import log_crypto_data
```

**Benefits:**
- API logic separated into its own module
- Clear imports from organized packages
- Better separation of concerns

---

### 2. `crypto_agent.py` → `src/crypto_monitor/agents/daily_agent.py`

**Old:**
```python
# crypto_agent.py (in project root)
from pydantic import BaseModel

class CryptoSummary(BaseModel):
    summary: str
    sentiment: str
    reasoning: str

model = OpenAIChatModel("gpt-4o-mini")
agent = Agent[CryptoSummary](model, system_prompt="...")

def summarize_crypto(text: str) -> CryptoSummary:
    # ...
```

**New:**
```python
# src/crypto_monitor/agents/daily_agent.py
from crypto_monitor.models import CryptoSummary
from crypto_monitor.utils import get_config

def _create_daily_agent() -> Agent:
    config = get_config()
    model = OpenAIChatModel(config.openai_model)
    # ...

def summarize_crypto(text: str) -> CryptoSummary:
    # ...
```

**Changes:**
- Models moved to `models/schemas.py`
- Configuration centralized in `utils/config.py`
- Agent creation separated into private function
- Better imports and organization

---

### 3. `crypto_logger.py` → `src/crypto_monitor/storage/sheets_logger.py`

**Old:**
```python
# crypto_logger.py (in project root)
CREDS_PATH = "crypto_creds.json"
SHEET_ID = "1funEXQuIcJDERgZ31b16rIbWj32GB-wJwnyt0PojHVA"

def get_gspread_client():
    creds = Credentials.from_service_account_file(CREDS_PATH, scopes=Scopes)
    return gspread.authorize(creds)
```

**New:**
```python
# src/crypto_monitor/storage/sheets_logger.py
from crypto_monitor.utils import get_config

def get_gspread_client() -> gspread.Client:
    config = get_config()
    creds = Credentials.from_service_account_file(
        str(config.creds_path),
        scopes=config.scopes
    )
    return gspread.authorize(creds)
```

**Changes:**
- Configuration loaded from centralized config
- Added type hints
- Better docstrings
- No hardcoded constants

---

### 4. `trend_analyzer.py` → `src/crypto_monitor/agents/weekly_agent.py`

**Old:**
```python
# trend_analyzer.py (in project root)
CREDS_PATH = "crypto_creds.json"
SHEET_ID = "1funEXQuIcJDERgZ31b16rIbWj32GB-wJwnyt0PojHVA"

class weeklyInsight(BaseModel):  # Note: lowercase 'w'
    summary: str
    sentiment: str
    reasoning: str

def analyze_week():
    # ... hardcoded sheet names ...
```

**New:**
```python
# src/crypto_monitor/agents/weekly_agent.py
from crypto_monitor.models import WeeklyInsight  # Renamed to PascalCase
from crypto_monitor.utils import get_config

def _create_weekly_agent() -> Agent:
    config = get_config()
    # ...

def analyze_week() -> None:
    config = get_config()
    # ... uses config.sheet_id, config.source_sheet_name, etc ...
```

**Changes:**
- Model renamed from `weeklyInsight` to `WeeklyInsight` (PascalCase)
- Configuration centralized
- Added type hints
- Private helper functions prefixed with `_`

---

## New Files Created

### `src/crypto_monitor/api/coingecko.py`

**Extracted from** `main.py`'s `fetch_crypto_prices()` function

**Purpose:** Dedicated API client module

**Benefits:**
- Can easily add more crypto sources (Binance, Kraken, etc.)
- Better error handling
- Easier to test and mock

---

### `src/crypto_monitor/models/schemas.py`

**Extracted from:** `crypto_agent.py` and `trend_analyzer.py`

**Contains:**
- `CryptoSummary` model
- `WeeklyInsight` model (renamed from `weeklyInsight`)

**Benefits:**
- All data models in one place
- Easy to add new models
- Better validation and documentation

---

### `src/crypto_monitor/utils/config.py`

**New file** - centralized configuration

**Replaces hardcoded values from:**
- `crypto_logger.py`: `CREDS_PATH`, `SHEET_ID`, `Scopes`
- `trend_analyzer.py`: `CREDS_PATH`, `SHEET_ID`, `SCOPES`
- `crypto_agent.py`: OpenAI model name

**Benefits:**
- Single source of truth
- Easy to change settings
- Environment variable support
- Validation on startup

---

## Testing the New Structure

### Before Removing Old Files

Test that the new structure works:

```bash
# Test daily monitoring
python scripts/daily_run.py

# Test weekly report
python scripts/weekly_report.py
```

### After Verifying

Once you've confirmed everything works, you can remove the old files:

```bash
# Backup first (optional)
mkdir old_files
mv main.py crypto_agent.py crypto_logger.py trend_analyzer.py old_files/

# Or delete directly
rm main.py crypto_agent.py crypto_logger.py trend_analyzer.py
```

---

## Import Changes Summary

### Old Way
```python
from crypto_agent import summarize_crypto
from crypto_logger import log_crypto_data
```

### New Way
```python
import sys
sys.path.insert(0, 'src')

from crypto_monitor.agents import summarize_crypto
from crypto_monitor.storage import log_crypto_data
```

---

## Configuration Changes

### Old Way
```python
# Hardcoded in each file
SHEET_ID = "1funEXQuIcJDERgZ31b16rIbWj32GB-wJwnyt0PojHVA"
model = OpenAIChatModel("gpt-4o-mini")
```

### New Way
```python
from crypto_monitor.utils import get_config

config = get_config()
sheet_id = config.sheet_id
model = OpenAIChatModel(config.openai_model)
```

### Environment Variables

Add to `.env`:
```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini  # Optional, defaults to gpt-4o-mini
SHEET_ID=your_sheet_id    # Optional, has default
```

---

## Benefits of New Structure

1. **Modular**: Each module has a single responsibility
2. **Testable**: Easy to test individual components
3. **Scalable**: Easy to add new features
4. **Maintainable**: Clear organization
5. **Professional**: Follows best practices
6. **Type-Safe**: Added type hints throughout
7. **Documented**: Comprehensive docstrings
8. **Configurable**: Centralized configuration

---

## Next Steps

1. Test the new structure thoroughly
2. Remove old files once confirmed working
3. Consider adding unit tests in `tests/`
4. Set up automation (cron jobs, GitHub Actions)
5. Add more features (new coins, notifications, etc.)

Need help? Check `README.md` and `STRUCTURE.md`!
