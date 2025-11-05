#!/usr/bin/env python3
"""Daily crypto monitoring script - fetches prices and logs AI analysis."""
import sys
from pathlib import Path

# Add src to path so we can import crypto_monitor
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from crypto_monitor.api import fetch_crypto_prices
from crypto_monitor.agents import summarize_crypto
from crypto_monitor.storage import log_crypto_data


def analyze_crypto(btc: float, eth: float) -> None:
    """Analyze crypto prices using AI and log the results.

    Args:
        btc: Bitcoin price in USD
        eth: Ethereum price in USD
    """
    text = f"Bitcoin is ${btc} and Ethereum is ${eth}. Summarize today's crypto trend and give sentiment."
    result = summarize_crypto(text)

    print("\n🧠 AI Summary:")
    print(result.summary)
    print("📊 Sentiment:", result.sentiment)

    log_crypto_data(
        btc=btc,
        eth=eth,
        summary=result.summary,
        sentiment=result.sentiment,
        reasoning=result.reasoning
    )

    return result


def main() -> None:
    """Main entry point for daily crypto monitoring."""
    print("🚀 Starting daily crypto monitoring...\n")

    try:
        # Fetch current prices
        btc, eth = fetch_crypto_prices()
        print(f"💰 BTC: ${btc:,.2f} | ETH: ${eth:,.2f}")

        # Analyze and log
        analyze_crypto(btc, eth)

        print("\n✅ Daily run completed successfully!")

    except Exception as e:
        print(f"\n❌ Error during daily run: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
