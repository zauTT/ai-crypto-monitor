import requests
from crypto_agent import summarize_crypto
from dotenv import load_dotenv

load_dotenv()

def fetch_crypto_prices():
    """Fetch real BTC and ETH prices from CoinGecko"""
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        btc = data["bitcoin"]["usd"]
        eth = data["ethereum"]["usd"]
        return btc, eth
    else:
        raise Exception(f"❌ Failed to fetch crypto prices: {res.status_code}")
    
def analyze_crypto(btc, eth):
    """Ask the AI agent to summerize today's trend."""
    text = f"Bitcoin is ${btc} and Ethereum is ${eth}. Summerize today's crypto trend and give sentiment."
    result = summarize_crypto(text)
    print("\n🧠 AI Summary:")
    print(result.summary)
    print("📊 Sentiment:", result.sentiment)
    return result

def main():
    btc, eth = fetch_crypto_prices()
    print(f"💰 BTC: ${btc} | ETH: ${eth}")
    analyze_crypto(btc, eth)

if __name__ == "__main__":
    main()
