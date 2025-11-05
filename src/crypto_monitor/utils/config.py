"""Configuration management for the crypto monitor."""
import os
from pathlib import Path
from typing import Optional


class Config:
    """Application configuration."""

    def __init__(self):
        # Project root directory (where .env is located)
        self.project_root = Path(__file__).parent.parent.parent.parent

        # API Configuration
        self.coingecko_api_url = "https://api.coingecko.com/api/v3/simple/price"

        # Google Sheets Configuration
        self.creds_path = self.project_root / "crypto_creds.json"
        self.sheet_id = os.getenv("SHEET_ID", "1funEXQuIcJDERgZ31b16rIbWj32GB-wJwnyt0PojHVA")
        self.source_sheet_name = "AI_Crypto_Log"
        self.target_sheet_name = "Weekly_Reports"

        # Google Sheets Scopes
        self.scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        # OpenAI Configuration
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        # Analysis Configuration
        self.weekly_analysis_days = 7

    def validate(self) -> bool:
        """Validate that required configuration is present."""
        if not self.creds_path.exists():
            raise FileNotFoundError(f"Credentials file not found: {self.creds_path}")

        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        return True


# Singleton instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get the application configuration singleton."""
    global _config
    if _config is None:
        _config = Config()
    return _config
