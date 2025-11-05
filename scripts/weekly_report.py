#!/usr/bin/env python3
"""Weekly crypto trend analysis script - analyzes last 7 days of data."""
import sys
from pathlib import Path

# Add src to path so we can import crypto_monitor
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from crypto_monitor.agents import analyze_week


def main() -> None:
    """Main entry point for weekly crypto analysis."""
    print("🚀 Starting weekly crypto analysis...\n")

    try:
        analyze_week()
        print("\n✅ Weekly analysis completed successfully!")

    except Exception as e:
        print(f"\n❌ Error during weekly analysis: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
