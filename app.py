from flask import Flask, request, jsonify
from bitunix_api import place_order
import config

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ Bitunix Trading Bot is Live!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    symbol = data.get("symbol")
    action = data.get("action")
    size = data.get("size")
    price = data.get("price")
    reason = data.get("reason", "signal")

    result = place_order(symbol, action, size, price, reason)
    return jsonify({"status": "ok", "result": result})

if __name__ == "__main__":
    app.run(debug=True)
