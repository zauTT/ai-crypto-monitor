import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel

CREDS_PATH = "crypto_creds.json"
SHEET_ID = "1funEXQuIcJDERgZ31b16rIbWj32GB-wJwnyt0PojHVA"
SOURCE_SHEET_NAME = "AI_Crypto_Log"
TARGET_SHEET_NAME = "Weekly_Reports"

# print("📄 Using sheet ID:", SHEET_ID)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# creds = Credentials.from_service_account_file(CREDS_PATH, scopes=SCOPES)
# client = gspread.authorize(creds)
# sheet = client.open_by_key(SHEET_ID)

# print("📄 Available sheet tabs:")
# for ws in sheet.worksheets():
#     print("-", ws.title)

def get_client():
    creds = Credentials.from_service_account_file(CREDS_PATH, scopes=SCOPES)
    return gspread.authorize(creds)

def get_last_n_rows(worksheet, n=7):
    """Return last n rows as list of dicts (assumes header in row 1)."""
    records = worksheet.get_all_records()
    if not records:
        return []
    return records[-n:]

class weeklyInsight(BaseModel):
    summary: str
    sentiment: str
    reasoning: str

model = OpenAIChatModel("gpt-4o-mini")

weekly_agent = Agent[weeklyInsight](
    model,
    system_prompt=(
        "You are a weekly crypto market analyst. "
        "I will give you the last few daily AI crypto logs with prices and sentiment. "
        "Your job is to write a 2–3 sentence weekly summary. "
        "Then classify the overall weekly sentiment as Bullish, Bearish, or Neutral. "
        "Finally, explain briefly (1 sentence) why you chose that sentiment. "
        "Output ONLY valid JSON:\n"
        "{\n"
        '  "summary": "...",\n'
        '  "sentiment": "...",\n'
        '  "reasoning": "..."\n'
        "}"
    ),
)

def analyze_week():
    client = get_client()
    sheet = client.open_by_key(SHEET_ID)

    try:
        src_ws = sheet.worksheet(SOURCE_SHEET_NAME)
    except gspread.WorksheetNotFound:
        print(f"❌ Source sheet '{SOURCE_SHEET_NAME}' not found.")
        return
    
    last_rows = get_last_n_rows(src_ws, n=7)
    if not last_rows:
        print("❌ No data found in AI_Crypto_Log..")
        return
    
    btc_values = []
    eth_values = []
    sentiment_counts = {"Bullish": 0, "Bearish": 0, "Neutral": 0}

    for row in last_rows:
        btc = row.get("BTC (USD)")
        eth = row.get("ETH (USD)")
        if isinstance(btc, (int, float)):
            btc_values.append(btc)
        if isinstance(eth, (int, float)):
            eth_values.append(eth)

    sent = row.get("Sentiment", "").strip()
    if sent in sentiment_counts:
        sentiment_counts[sent] += 1

    avg_btc = sum(btc_values) / len(btc_values) if btc_values else 0.0
    avg_eth = sum(eth_values) / len(eth_values) if eth_values else 0.0

    recent_text = "Recent crypto logs (latest first):\n"
    for r in last_rows:
        recent_text += (
            f"- {r.get('Timestamp')}: BTC={r.get('BTC (USD)')}, "
            f"ETH={r.get('ETH (USD)')}, Sentiment={r.get('Sentiment')}, "
            f"Reasoning={r.get('Reasoning')}\n"
        )

    prompt = f"""
Here are the last {len(last_rows)} crypto logs:
{recent_text}

Stats:
- Average BTC price: ${avg_btc:.2f}
- Average ETH price: ${avg_eth:.2f}
- Sentiment counts: {sentiment_counts}

Based on this, write a weekly summary.
"""
    
    try:
        resp = weekly_agent.run_sync(prompt)
        print("\n🧠 Raw AI weekly output:", resp.output)

        if isinstance(resp.output, str):
            parsed = weeklyInsight.model_validate_json(resp.output)
        else:
            parsed = weeklyInsight.model_validate(resp.output)

    except Exception as e:
        print(f"❌ Failed to generate structured output: {e}")
        parsed = weeklyInsight(
            summary="Weekly crypto report generated, but AI could not parse structured output.",
            sentiment="Unknown",
            reasoning="AI returned non-JSON output."
        )

    try:
        target_ws = sheet.worksheet(TARGET_SHEET_NAME)
    except gspread.WorksheetNotFound:
        target_ws = sheet.add_worksheet(title=TARGET_SHEET_NAME, rows="200", cols="10")
        target_ws.append_row([
            "Date",
            "Avg BTC",
            "Avg ETH",
            "Bullish",
            "Bearish",
            "Neutral",
            "Weekly Sentiment",
            "Reasoning",
            "Summary",
        ])

    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    target_ws.append_row([
        today,
        avg_btc,
        avg_eth,
        sentiment_counts["Bullish"],
        sentiment_counts["Bearish"],
        sentiment_counts["Neutral"],
        parsed.sentiment,
        parsed.reasoning,
        parsed.summary,
    ])

    print("\n✅ Weekly report saved to Google Sheets (Weekly_Reports).")
    print("📊 Averages:", f"BTC={avg_btc:.2f}", f"ETH={avg_eth:.2f}")
    print("🧭 Sentiments:", sentiment_counts)
    print("📝 AI Summary:", parsed.summary)

if __name__ == "__main__":
    analyze_week()