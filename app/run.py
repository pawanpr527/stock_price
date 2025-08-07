from flask import Flask,redirect,render_template,request,url_for,jsonify
import redis
import sys
sys.path.append('src')
from data_loader import data_load
from src.model import prediction
from src.data_loader import data_load
app = Flask(__name__)
import yfinance as yf


app.secret_key = "pawan236007"

r = redis.Redis(host='localhost',port=6379,db=0,decode_responses=True)

indian_stocks = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS",
    "ICICIBANK.NS", "HINDUNILVR.NS", "SBIN.NS", "LT.NS",
    "AXISBANK.NS", "KOTAKBANK.NS", "BHARTIARTL.NS", "ITC.NS", "MARUTI.NS",
    "HCLTECH.NS", "WIPRO.NS", "TATAMOTORS.NS", "BAJFINANCE.NS", "ASIANPAINT.NS",
    "NTPC.NS", "POWERGRID.NS", "COCHINSHIP.NS", "GRSE.NS", "BSE.NS",
    "CYIENT.NS", "ADANIPOWER.NS"
]
indian_stocks = [i.replace('.NS','') for i in indian_stocks]

company_map = {
    "Reliance Industries": "RELIANCE.NS", "TCS": "TCS.NS","HDFC Bank": "HDFCBANK.NS",
    "Infosys": "INFY.NS","ICICI Bank": "ICICIBANK.NS","Hindustan Unilever": "HINDUNILVR.NS",
    "State Bank of India": "SBIN.NS","Larsen & Toubro": "LT.NS",
    "Axis Bank": "AXISBANK.NS","Kotak Mahindra Bank": "KOTAKBANK.NS","Bharti Airtel": "BHARTIARTL.NS",
    "ITC": "ITC.NS","Maruti Suzuki": "MARUTI.NS",
    "HCL Technologies": "HCLTECH.NS","Wipro": "WIPRO.NS","Tata Motors": "TATAMOTORS.NS",
    "Bajaj Finance": "BAJFINANCE.NS","Asian Paints": "ASIANPAINT.NS",
    "NTPC": "NTPC.NS","Power Grid": "POWERGRID.NS",
    "Cochin Shipyard": "COCHINSHIP.NS","Garden Reach Shipbuilders": "GRSE.NS",
    "BSE Ltd": "BSE.NS","Cyient": "CYIENT.NS",
    "Adani Power": "ADANIPOWER.NS"
}


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/suggest')
def suggest():
    query = request.args.get('q', '').strip().lower()
    results = []

    for name, symbol in company_map.items():
        if query in name.lower() or query in symbol.lower():
            results.append({'name': name, 'symbol': symbol})

    return jsonify(results)


@app.route('/dashboard/<symbol>')
def dashboard(symbol):
    try:
        symbol = symbol.upper().replace(".NS", "")
        stock_full = f"{symbol}.NS"

        # Predict next day's price
        predicted_price = prediction(symbol)

        # Fetch latest 10 days data
        df = yf.Ticker(stock_full).history(period="5y")  # Get at least 7 days for moving average
        df.reset_index(inplace=True)
        if df.empty:
            return f"No data found for symbol {stock_full}", 404

        # Latest row (last day)
        latest = df.iloc[-1]
        latest_open = round(latest['Open'], 2)
        latest_close = round(latest['Close'], 2)
        latest_high = round(latest['High'], 2)
        latest_volume = int(latest['Volume'])

        # Add 7-day moving average
        df['7ma'] = df['Close'].rolling(window=7).mean()

        # Extract data for chart
        dates = df['Date'].tail(300).dt.strftime('%Y-%m-%d').tolist()
        closes = df['Close'].tail(300).round(2).fillna('').tolist()
        volumes = df['Volume'].tail(300).fillna(0).astype(int).tolist()
        moving_avg = df['7ma'].tail(300).round(2).fillna('').tolist()

        # Optional historical table
        historical_data_df = df[['Date', 'Open', 'Close', 'High', 'Volume']].copy()
        historical_data_df['Date'] = historical_data_df['Date'].dt.strftime('%Y-%m-%d')
        return render_template('dashboard.html',
            name=symbol,
            Open=latest_open,
            Close=latest_close,
            High=latest_high,
            Volume=latest_volume,
            price=round(predicted_price, 2),
            dates=dates,
            closes=closes,
            volumes=volumes,
            moving_avg=moving_avg,
            historical_data=historical_data_df.tail(100).to_dict(orient='records')
        )

    except Exception as e:
        return f"Error: {e}", 500





if __name__=="__main__":
    app.run(host='0.0.0.0',port=5001,debug=True)
