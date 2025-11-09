from flask import Flask, redirect, request, render_template
from itertools import cycle
import requests
import os

app = Flask(__name__)

# Backend servers
servers = [
    "https://l1-11.onrender.com/",
    "https://l1-s2.onrender.com/",
    "https://l1-s3.onrender.com/"
]

# Create an endless cycle (round robin)
server_cycle = cycle(servers)

@app.route('/', methods=['GET', 'POST'])
def loadbalancer():
    if request.method == 'POST':
        topic = request.form.get('topic', '').strip()

        if not topic:
            return render_template("index.html", error="Please enter a topic.", server="loadbalancer")

        # Try each backend server in order
        for ser in servers:
            try:
                resp = requests.post(ser, data={"topic": topic}, timeout=5)

                # if backend didn't return JSON, skip
                try:
                    data = resp.json()
                except ValueError:
                    continue

                if resp.status_code == 200:
                    server_name = (
                        "server1" if "l1-11" in ser else
                        "server2" if "l1-s2" in ser else
                        "server3"
                    )

                    return render_template(
                        "index.html",
                        topic=data.get("topic"),
                        summary=data.get("summary", []),
                        urls_found=data.get("urls_found", []),
                        error=data.get("error"),
                        server=server_name
                    )

            except requests.exceptions.RequestException as e:
                print(f"⚠️ {ser} failed: {e}")
                continue  # Try next server

        # If all backends failed
        return render_template("index.html", error="All backend servers failed!", server="loadbalancer")

    # For GET request
    return render_template("index.html", server="loadbalancer")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
