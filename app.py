from flask import Flask, render_template, request, jsonify
from tradingview_ta import TA_Handler, Interval
import requests
import pandas as pd
import numpy as np
import datetime

app = Flask(__name__)

# List of currency pairs
pairs = ["GBPUSD", "EURUSD", "USDJPY", "AUDUSD", "USDCAD", "USDCHF", "NZDUSD", "EURGBP", "EURJPY", "GBPJPY"]

def verify_password(password):
    lifetime_password = "Nts@ko123"
    temporary_password = "0000"
    current_date = datetime.datetime.now()
    expiry_date = datetime.datetime(2025, 1, 1)
    
    if password == lifetime_password:
        return True
    elif password == temporary_password and current_date < expiry_date:
        return True
    else:
        return False

def get_pair_analysis(pair):
    handler = TA_Handler(
        symbol=pair,
        screener="forex",
        exchange="FX",
        interval=Interval.INTERVAL_15_MINUTES
    )
    analysis = handler.get_analysis()
    signal = analysis.summary['RECOMMENDATION']
    
    return signal

def get_current_price(pair, api_key):
    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={pair[:3]}&to_currency={pair[3:]}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    try:
        current_price = float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
    except KeyError:
        current_price = None

    return current_price

def get_atr(pair, api_key):
    symbol = pair[:3] + pair[3:]
    url = f"https://www.alphavantage.co/query?function=ATR&symbol={symbol}&interval=5min&time_period=10&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    try:
        latest_timestamp = next(iter(data["Technical Analysis: ATR"]))
        atr = float(data["Technical Analysis: ATR"][latest_timestamp]["ATR"])
    except (KeyError, StopIteration):
        atr = None

    return atr

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        password = request.form.get('password')
        if not verify_password(password):
            message = "Please make sure you have made your purchase with Ntsako Khumalo at ntsakokhumalo123@gmail.com or WhatsApp the institution at +27628082902"
            return render_template('index.html', pairs=pairs, result='', message=message)

        pair = request.form.get('pair')
        api_key = request.form.get('api_key')
        
        signal = get_pair_analysis(pair)
        current_price = get_current_price(pair, api_key)
        atr = get_atr(pair, api_key)

        if current_price is None or atr is None:
            result = f"Failed to fetch current price or ATR for {pair}"
        else:
            take_profit = round(current_price + (atr * 2), 5)
            stop_loss = round(current_price - atr, 5)
            
            result = f"""
            Pair: {pair}<br>
            Signal: {signal}<br>
            Current Price: {current_price}<br>
            Average True Range (ATR): {atr}<br>
            Take Profit (TP): {take_profit}<br>
            Stop Loss (SL): {stop_loss}<br>
            -------------------------------------
            """

        return render_template('index.html', pairs=pairs, result=result, message='')
    return render_template('index.html', pairs=pairs, result='', message='')

if __name__ == '__main__':
    app.run(debug=True)