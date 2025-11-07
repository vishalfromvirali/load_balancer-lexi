from flask import Flask,jsonify
import requests,os
from itertools import cycle


app=Flask(__name__)

servers=['https://l1-11.onrender.com/', 'https://l1-s2.onrender.com/','https://l1-s3.onrender.com/']
server=cycle(servers)


@app.route('/')
def loadbalancer():
    server_data=next(server)
    copy=server_data
    try:
        return requests.get(server_data).text
    except:
        server_data=next(server)
        try:
            res=requests.get(server_data).text
            res+="  --   "+copy +" :     -- this server have error"
            return res
        except:
            return "server {server_data} have error"
        
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)