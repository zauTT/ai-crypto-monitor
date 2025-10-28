from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel

class CryptoSummary(BaseModel):
    summary: str
    sentiment: str

model = OpenAIChatModel("gpt-4o-mini")

agent = Agent[CryptoSummary](
    model,
    system_prompt=(
        "You are crypto analyst. "
        "Summerize Bitcoin and Ethereum price movements clearly in 1-2 sentences. "
        "Classify the overall market sentiment as Bullish, Bearish, or Neutral."
    ),
)

def summarize_crypto(text: str) -> CryptoSummary:
    """
    Run the agent on a crypto trend text and returns stuctured summery.
    """
    response = agent.run_sync(text)
    print("\n🧠 Raw AI output:", response.output)
    try:
        data = CryptoSummary.model_validate(response.output)
        print("✅ Parsed structured output:", data)
        return data
    except Exception:
        print("⚠️ Could not parse JSON, returning raw string instead.")
        return CryptoSummary(summary=response.output, sentiment="Unknown")
    
if __name__ == "__main__":
    sample_input = "Bitcoin rose 2% today while Ethereum fell slightly by 0.5%. Market mood seens mixed."
    result = summerize_crypto(sample_input)
    print("\n🧩 As dict:", result.model_dump())
