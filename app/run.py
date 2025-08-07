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

@app.route('/registration',methods=['GET','POST'])
def register():
  if request.method=="POST":  
    name = request.form.get('First')
    last = request.form.get('Last')
    email = request.form.get('Email')
    password = request.form.get('Password')
    r.hset(f"user:{email}",
      mapping={
          'first' : name,
          'last' : last,
          'password' : password,
          'email' : email
      }
    )
    return redirect(url_for('index'))
  return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user_key = f"user:{email}"
        if r.exists(user_key):
            storedpass = r.hget(user_key, 'password')
            if password == storedpass:
                return redirect(url_for('index'))
            else:
                return "Incorrect password"
        else:
            return "Email not registered"

    # For GET request, show login form
    return render_template('login.html')

if __name__=="__main__":
    app.run(host='0.0.0.0',port=5001,debug=True)
