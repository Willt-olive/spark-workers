from flask import Flask, jsonify, send_file
from flask import request
import requests
import os
import json
app = Flask(__name__)

def get_api_key() -> str:
    secret = os.environ.get("COMPUTE_API_KEY_2")
    if secret:
        return secret
    else:
        #local testing
        with open('.key') as f:
            return f.read()
      
@app.route("/")
def hello():
    return send_file(os.path.join(os.path.dirname(__file__), 'index.html'))

@app.route("/test")
def test():
    #return "Test" # testing 
    return(get_api_key())

@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return "Use post to add"  # replace with form template
    elif request.method == 'POST':
        try:
            data = request.get_json()
            num = data['num']
            token = get_api_key()
            ret = addWorker(token, num)
            return jsonify({"result": ret})
        except Exception as e:
            return jsonify({"error": str(e)}), 400


def addWorker(token, num):
    with open('payload.json') as p:
      tdata=json.load(p)
    tdata['name']='slave'+str(num)
    data=json.dumps(tdata)
    url='https://www.googleapis.com/compute/v1/projects/calm-library-407909/zones/europe-west2-c/instances'
    headers={"Authorization": "Bearer "+token}
    resp=requests.post(url,headers=headers, data=data)
    if resp.status_code==200:     
      return "Done"
    else:
      print(resp.content)
      return "Error\n"+resp.content.decode('utf-8') + '\n\n\n'+data



if __name__ == "__main__":
    app.run(host='0.0.0.0',port='8080')
