
from flask import Flask, request, jsonify
import time
import logging

app = Flask(__name__)

# 設定 logging（Render Logs 可見）
logging.basicConfig(level=logging.INFO)

@app.route("/")
def index():
    return "Bitunix Maker Bot Online"

@app.route("/maker", methods=["POST"])
def maker():
    data = request.json
    app.logger.info("🟢 收到 Webhook 訊號：%s", data)

    results = {
        "BTCUSDT": {"status": "success", "orderId": f"demo-{int(time.time())}"},
        "ETHUSDT": {"status": "success", "orderId": f"demo-{int(time.time())}"},
        "SOLUSDT": {"status": "success", "orderId": f"demo-{int(time.time())}"}
    }

    app.logger.info("✅ 已模擬掛單結果：%s", results)

    return jsonify({"message": "已處理掛單", "results": results})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
