from flask import Flask, redirect
from itertools import cycle
import os

app = Flask(__name__)

servers = [
    'https://l1-11.onrender.com/',
    'https://l1-s2.onrender.com/',
    'https://l1-s3.onrender.com/'
]

server_cycle = cycle(servers)

@app.route('/')
def loadbalancer():
    next_server = next(server_cycle)
    return redirect(next_server)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
