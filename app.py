
from flask import Flask, request, jsonify
import time

app = Flask(__name__)

@app.route("/")
def index():
    return "Bitunix Maker Bot Online"

@app.route("/maker", methods=["POST"])
def maker():
    # 模擬回應處理掛單
    results = {
        "BTCUSDT": {"status": "success", "orderId": f"demo-{int(time.time())}"},
        "ETHUSDT": {"status": "success", "orderId": f"demo-{int(time.time())}"},
        "SOLUSDT": {"status": "success", "orderId": f"demo-{int(time.time())}"}
    }
    return jsonify({"message": "已處理掛單", "results": results})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
