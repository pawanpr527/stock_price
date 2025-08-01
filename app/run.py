import pandas as pd
import yfinance as yf
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
import time

# Step 1: List of proxies (use real proxies here)
proxies = [
    "http://your_proxy_1:port",
    "http://your_proxy_2:port",
    # Add more proxies here
]

# Step 2: Create session with proxy
def get_yf_with_proxy(proxy_url):
    session = requests.Session()
    session.proxies = {
        'http': proxy_url,
        'https': proxy_url
    }
    return yf.shared._TickerBase._get_fundamentals.session.__class__(), session

# Step 3: Fetch function
def fetch_data(symbol, proxy):
    try:
        # Create session with proxy
        session = requests.Session()
        session.proxies = {
            'http': proxy,
            'https': proxy
        }

        ticker = yf.Ticker(symbol, session=session)
        df = ticker.history(period="max")

        if df.empty:
            return f"{symbol} ➤ ⚠️ No data found"
        else:
            return f"{symbol} ➤ ✅ Data fetched\n{df.head(2)}"
    except Exception as e:
        return f"{symbol} ➤ ❌ Error: {e}"

# Step 4: Load symbols
data = pd.read_csv("data/valid_yahoo_symbols.csv")
symbols = [x + ".NS" for x in data["ValidSymbols"].tolist()]

# Step 5: Threaded fetch
max_threads = 10  # Adjust based on CPU and network
results = []

with ThreadPoolExecutor(max_workers=max_threads) as executor:
    futures = []

    for i, symbol in enumerate(symbols[:50]):  # Limit to first 50 for test
        proxy = random.choice(proxies)
        futures.append(executor.submit(fetch_data, symbol, proxy))

    for future in as_completed(futures):
        print(future.result())

# from concurrent.futures import ThreadPoolExecutor, as_completed
# from tqdm import tqdm

# raw_df = pd.read_csv("data/Nse_symbols.csv")
# raw_symbols = raw_df['Symbols'].dropna().astype(str).tolist()
# yahoo_symbols = [s.strip().upper() + ".NS" for s in raw_symbols]

# valid_symbols = []

# def check_symbol(sym):
#     try:
#         ticker = yf.Ticker(sym)
#         hist = ticker.history(period="5d")
#         if not hist.empty:
#             return sym
#     except:
#         return None

# print("🔍 Checking symbols using multithreading...\n")

# with ThreadPoolExecutor(max_workers=20) as executor:
#     futures = {executor.submit(check_symbol, sym): sym for sym in yahoo_symbols}
#     for future in tqdm(as_completed(futures), total=len(yahoo_symbols)):
#         result = future.result()
#         if result:
#             valid_symbols.append(result)

# clean_symbols = [s.replace(".NS", "") for s in valid_symbols]
# pd.DataFrame({'ValidSymbols': clean_symbols}).to_csv("data/valid_yahoo_symbols.csv", index=False)

# print(f"\n✅ {len(valid_symbols)} valid symbols saved to 'data/valid_yahoo_symbols.csv'")
