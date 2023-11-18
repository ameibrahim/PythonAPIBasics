from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/calculate/", methods=['GET'])
def calculate():

    result = {
        "result": 0
    }

    a = request.args.get("a")
    b = request.args.get("b")

    if a != None and b != None :
      result["result"] = int(a) + int(b)
    
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    

if __name__ == "__main__":
    app.run()