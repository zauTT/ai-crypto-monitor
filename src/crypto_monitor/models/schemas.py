"""Pydantic models for data validation and structure."""
from pydantic import BaseModel, Field


class CryptoSummary(BaseModel):
    """Model for daily crypto market analysis."""

    summary: str = Field(..., description="Brief market summary (1-2 sentences)")
    sentiment: str = Field(..., description="Market sentiment: Bullish, Bearish, or Neutral")
    reasoning: str = Field(..., description="Brief explanation for the sentiment")


class WeeklyInsight(BaseModel):
    """Model for weekly crypto market analysis."""

    summary: str = Field(..., description="Weekly market summary (2-3 sentences)")
    sentiment: str = Field(..., description="Overall weekly sentiment: Bullish, Bearish, or Neutral")
    reasoning: str = Field(..., description="Brief explanation for the weekly sentiment")
