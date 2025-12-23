from flask import Flask, request, jsonify, render_template_string
import os
from openai import OpenAI

# ======================
# MekhaeeL AI
# ======================
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="ar">
<head>
<meta charset="UTF-8">
<title>MekhaeeL AI</title>
<style>
body{
  font-family:Arial;
  background:#0f172a;
  color:white;
  display:flex;
  justify-content:center;
  align-items:center;
  height:100vh;
}
.chat{
  width:420px;
  background:#020617;
  border-radius:12px;
  padding:12px;
}
.header{
  text-align:center;
  font-weight:bold;
  color:#38bdf8;
  margin-bottom:10px;
}
.msg{
  margin:6px 0;
  padding:8px 10px;
  border-radius:8px;
}
.user{
  background:#2563eb;
  text-align:right;
}
.bot{
  background:#334155;
}
input{
  width:100%;
  padding:10px;
  border-radius:6px;
  border:none;
  margin-top:10px;
}
</style>
</head>

<body>
<div class="chat">
  <div class="header">🤖 MekhaeeL AI</div>
  <div id="box"></div>
  <input id="input" placeholder="اكتب سؤالك واضغط Enter">
</div>

<script>
const box=document.getElementById("box");
const input=document.getElementById("input");

input.addEventListener("keypress", async e=>{
  if(e.key==="Enter"){
    let t=input.value;
    if(!t) return;

    box.innerHTML += `<div class='msg user'>${t}</div>`;
    input.value="";

    let r = await fetch("/chat",{
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({message:t})
    });

    let d = await r.json();
    box.innerHTML += `<div class='msg bot'>${d.reply}</div>`;
  }
});
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json["message"]

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role":"system","content":"أنت MekhaeeL AI، مساعد ذكي يتكلم عربي بطريقة ودودة وواضحة."},
            {"role":"user","content": user_msg}
        ]
    )

    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run()