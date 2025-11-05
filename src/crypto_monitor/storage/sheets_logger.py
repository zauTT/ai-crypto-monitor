"""Google Sheets logging functionality."""
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

from crypto_monitor.utils import get_config


def get_gspread_client() -> gspread.Client:
    """Get authorized Google Sheets client.

    Returns:
        gspread.Client: Authorized client for Google Sheets API
    """
    config = get_config()
    creds = Credentials.from_service_account_file(str(config.creds_path), scopes=config.scopes)
    return gspread.authorize(creds)


def log_crypto_data(
    btc: float,
    eth: float,
    summary: str,
    sentiment: str,
    reasoning: str
) -> None:
    """Append crypto data with AI analysis to Google Sheets.

    Args:
        btc: Bitcoin price in USD
        eth: Ethereum price in USD
        summary: AI-generated market summary
        sentiment: Market sentiment (Bullish, Bearish, or Neutral)
        reasoning: Explanation for the sentiment

    Example:
        >>> log_crypto_data(65000, 3200, "Market is up", "Bullish", "Strong upward trend")
        ✅ Logged to AI_Crypto_Log at 2024-10-30 12:00:00
    """
    config = get_config()
    client = get_gspread_client()

    spreadsheet = client.open_by_key(config.sheet_id)

    # Get or create the worksheet
    try:
        worksheet = spreadsheet.worksheet(config.source_sheet_name)
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(
            title=config.source_sheet_name,
            rows="1000",
            cols="6"
        )
        # Add header row
        worksheet.append_row([
            "Timestamp",
            "BTC (USD)",
            "ETH (USD)",
            "Sentiment",
            "Reasoning",
            "Summary"
        ])

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    worksheet.append_row([timestamp, btc, eth, sentiment, reasoning, summary])
    print(f"✅ Logged to {config.source_sheet_name} at {timestamp}")
