#!/usr/bin/env python3
"""
Quick shortcut to run daily monitoring.
Usage: python3 run.py
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import and run
from crypto_monitor.api import fetch_crypto_prices
from crypto_monitor.agents import summarize_crypto
from crypto_monitor.storage import log_crypto_data


def main():
    """Run daily crypto monitoring."""
    print("🚀 Starting crypto monitoring...\n")

    # Fetch prices
    btc, eth = fetch_crypto_prices()
    print(f"💰 BTC: ${btc:,.2f} | ETH: ${eth:,.2f}")

    # Analyze
    text = f"Bitcoin is ${btc} and Ethereum is ${eth}. Summarize today's crypto trend and give sentiment."
    result = summarize_crypto(text)

    print("\n🧠 AI Summary:")
    print(result.summary)
    print("📊 Sentiment:", result.sentiment)

    # Log to Google Sheets
    log_crypto_data(btc, eth, result.summary, result.sentiment, result.reasoning)

    print("\n✅ Done!")


if __name__ == "__main__":
    main()
