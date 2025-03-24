
import requests
import json
from flask import Flask

app = Flask(__name__)

with open('config.json') as f:
    config = json.load(f)

def send_line_notify(message):
    token = config.get("line_notify_token")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {"message": message}
    requests.post("https://notify-api.line.me/api/notify", headers=headers, data=payload)

@app.route("/test-line")
def test_line():
    send_line_notify("✅ 測試成功！LINE Notify 已連線！")
    return "LINE Notify 測試已送出"
