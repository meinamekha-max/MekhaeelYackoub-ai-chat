
from flask import Flask,request,jsonify,send_from_directory
from openai import OpenAI
import os

app = Flask(__name__, static_folder=".")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

FREE_LIMIT = 5
FREE_CODES = ["MEKHA-FREE"]
users = {}

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user = request.remote_addr
    code = request.headers.get("X-FREE-CODE")

    if code in FREE_CODES:
        allowed = True
    else:
        users[user] = users.get(user, 0) + 1
        allowed = users[user] <= FREE_LIMIT

    if not allowed:
        return jsonify({"paywall": True})

    msg = request.json["message"]
    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
          {"role":"system","content":"You are an AI inspired by FC Barcelona philosophy."},
          {"role":"user","content":msg}
        ]
    )
    return jsonify({"reply": res.choices[0].message.content})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
