from flask import Flask, redirect, request, render_template
from itertools import cycle
import requests
import os

app = Flask(__name__)

servers = [
    "https://l1-11.onrender.com/",
       "https://l1-s2.onrender.com/" ,
         "https://l1-s3.onrender.com/"  # Backend server URL
]

server_cycle = cycle(servers)

@app.route('/', methods=['GET', 'POST'])
def loadbalancer():
    next_server = next(server_cycle)

    if request.method == 'POST':
        topic = request.form.get('topic', '').strip()

        if not topic:
            return render_template("index.html", error="Please enter a topic.")

        # Send topic to backend
        try:
            resp = requests.post(next_server, data={"topic": topic})
            data = resp.json()
        except Exception as e:
            return render_template("index.html", error=f"Backend error: {e}")

        return render_template(
            "index.html",
            topic=data.get("topic"),
            summary=data.get("summary", []),
            urls_found=data.get("urls_found", []),
            error=data.get("error")
        )

    return render_template("index.html")
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
