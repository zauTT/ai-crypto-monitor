from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
import json

class CryptoSummary(BaseModel):
    summary: str
    sentiment: str
    reasoning: str

model = OpenAIChatModel("gpt-4o-mini")

agent = Agent[CryptoSummary](
    model,
    system_prompt=(
        "You are a professional crypto market analyst. "
        "Given Bitcoin and Ethereum prices or recent trends, summarize the market in 1–2 sentences. "
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
    """
    Analyze crypto data and return structured insight (summary, sentiment, reasoning).
    """
    response = agent.run_sync(text)
    print("\n🧠 Raw AI output:", response.output)
    try:
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
            summary=response.output,
            sentiment="Unknown",
            reasoning="AI output not structured."
        )
    
if __name__ == "__main__":
    sample_input = "Bitcoin rose 2% today while Ethereum fell slightly by 0.5%. Market mood seens mixed."
    result = summarize_crypto(sample_input)
    print("\n🧩 As dict:", result.model_dump())
