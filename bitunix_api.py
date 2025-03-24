import time
import hmac
import hashlib
import requests
import config

BASE_URL = "https://fapi.bitunix.com"

def get_timestamp():
    return str(int(time.time() * 1000))

def sign(params, secret):
    query = "&".join([f"{k}={v}" for k, v in sorted(params.items())])
    return hmac.new(secret.encode(), query.encode(), hashlib.sha256).hexdigest()

def place_order(symbol, action, size, price, reason):
    endpoint = "/api/v1/order/place"
    url = BASE_URL + endpoint

    side = "BUY" if action == "buy" else "SELL"
    positionSide = "LONG" if side == "BUY" else "SHORT"

    params = {
        "symbol": symbol,
        "side": side,
        "positionSide": positionSide,
        "type": "LIMIT",
        "price": str(price),
        "vol": str(size),
        "leverage": 100,
        "openType": "ISOLATED",
        "timestamp": get_timestamp()
    }
    params["sign"] = sign(params, config.API_SECRET)

    headers = {
        "Content-Type": "application/json",
        "X-BX-APIKEY": config.API_KEY
    }

    response = requests.post(url, json=params, headers=headers)
    return response.json()
