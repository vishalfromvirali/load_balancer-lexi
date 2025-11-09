from flask import Flask, render_template, request
from itertools import cycle
import requests
import os

app = Flask(__name__)

# List of backend servers
servers = [
    "https://l1-11.onrender.com/",
    "https://l1-s2.onrender.com/",
    "https://l1-s3.onrender.com/"
]

# Create a round robin cycle iterator
server_cycle = cycle(servers)

@app.route('/', methods=['GET', 'POST'])
def loadbalancer():
    if request.method == 'POST':
        topic = request.form.get('topic', '').strip()

        if not topic:
            return render_template("index.html", error="Please enter a topic.", server="loadbalancer")

        # Try each backend server in round robin order
        for _ in range(len(servers)):
            server = next(server_cycle)
            try:
                # Send POST request to backend
                resp = requests.post(server, data={"topic": topic}, timeout=5)
                data = resp.json()

                # Identify which server responded
                if server == "https://l1-11.onrender.com/":
                    server_name = "Server 1"
                elif server == "https://l1-s2.onrender.com/":
                    server_name = "Server 2"
                else:
                    server_name = "Server 3"

                # Return data to frontend
                return render_template(
                    "index.html",
                    topic=data.get("topic"),
                    summary=data.get("summary", []),
                    urls_found=data.get("urls_found", []),
                    error=data.get("error"),
                    server=server_name
                )
            except Exception as e:
                print(f"❌ {server} failed: {e}")
                continue  # Try next server

        # If all servers fail
        return render_template("index.html", error="All backend servers failed!", server="loadbalancer")

    # For GET request
    return render_template("index.html", server="loadbalancer")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

