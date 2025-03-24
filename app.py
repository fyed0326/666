from flask import Flask, request, jsonify
import requests
import time
import hmac
import hashlib
import json

app = Flask(__name__)

API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"
BASE_URL = "https://fapi.bitunix.com"

# 下單設定
MAX_POSITIONS = 20
TAKE_PROFIT = 0.8  # %
STOP_LOSS = -0.5  # %
POSITION_SIZE = 0.1  # BTC
active_positions = []
cooldown_tracker = {}

def get_price(symbol):
    try:
        url = f"{BASE_URL}/api/v1/market/ticker/price?symbol={symbol}"
        res = requests.get(url)
        return float(res.json()['data']['price'])
    except:
        return None

def sign(params):
    query = '&'.join([f"{k}={v}" for k, v in sorted(params.items())])
    signature = hmac.new(API_SECRET.encode(), query.encode(), hashlib.sha256).hexdigest()
    return signature

def place_order(symbol, side, size):
    timestamp = int(time.time() * 1000)
    params = {
        "symbol": symbol,
        "side": side.upper(),
        "type": "MARKET",
        "size": size,
        "timestamp": timestamp
    }
    params["sign"] = sign(params)
    headers = {"X-BX-APIKEY": API_KEY}
    url = f"{BASE_URL}/api/v1/order/place"
    r = requests.post(url, headers=headers, json=params)
    return r.json()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    symbol = data.get("symbol")
    action = data.get("action")
    size = data.get("size", POSITION_SIZE)

    if len(active_positions) >= MAX_POSITIONS:
        return jsonify({"status": "exceed_max_positions"})

    current_price = get_price(symbol)
    if not current_price:
        return jsonify({"status": "price_error"})

    result = place_order(symbol, action, size)
    active_positions.append({
        "symbol": symbol,
        "side": action,
        "entry": current_price,
        "size": size,
        "time": time.time()
    })

    print(f"✅ 下單成功: {result}")
    return jsonify({"message": "已處理", "result": result})

@app.route('/')
def index():
    return "✅ Bitunix 自動下單機器人已啟動"

if __name__ == '__main__':
    app.run(debug=True)
