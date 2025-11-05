"""Daily crypto market analysis agent."""
import json
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel

from crypto_monitor.models import CryptoSummary
from crypto_monitor.utils import get_config


def _create_daily_agent() -> Agent:
    """Create and configure the daily analysis agent."""
    config = get_config()
    model = OpenAIChatModel(config.openai_model)

    return Agent[CryptoSummary](
        model,
        system_prompt=(
            "You are a professional crypto market analyst. "
            "Given Bitcoin and Ethereum prices or recent trends, summarize the market in 1-2 sentences. "
            "Then classify the sentiment as Bullish, Bearish, or Neutral. "
            "Finally, explain your reasoning briefly (1 sentence). "
            "Output ONLY valid JSON in this format:\n\n"
            "{\n"
            '  "summary": "...",\n'
            '  "sentiment": "...",\n'
            '  "reasoning": "..."\n'
            "}"
        ),
    )


def summarize_crypto(text: str) -> CryptoSummary:
    """Analyze crypto data and return structured insight.

    Args:
        text: Description of current crypto market conditions

    Returns:
        CryptoSummary: Structured analysis with summary, sentiment, and reasoning

    Example:
        >>> result = summarize_crypto("Bitcoin is $65000 and Ethereum is $3200.")
        >>> print(result.sentiment)
        'Bullish'
    """
    agent = _create_daily_agent()
    response = agent.run_sync(text)

    print("\n🧠 Raw AI output:", response.output)

    try:
        # Parse the response
        if isinstance(response.output, str):
            data = json.loads(response.output)
        else:
            data = response.output

        validated = CryptoSummary.model_validate(data)

        print("\n✅ Parsed structured output:")
        print("📄 Summary:", validated.summary)
        print("📊 Sentiment:", validated.sentiment)
        print("💭 Reasoning:", validated.reasoning)

        return validated

    except Exception as e:
        print(f"⚠️ Could not parse structured JSON ({e}), returning raw string instead.")
        return CryptoSummary(
            summary=str(response.output),
            sentiment="Unknown",
            reasoning="AI output not structured."
        )


if __name__ == "__main__":
    # Test the agent
    sample_input = "Bitcoin rose 2% today while Ethereum fell slightly by 0.5%. Market mood seems mixed."
    result = summarize_crypto(sample_input)
    print("\n🧩 As dict:", result.model_dump())
