from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/get-user/<user_id>")
def get_user(user_id):
    
    user_data = {
        "user_id": user_id
    }

    extra = request.args.get("extra")

    if extra:
      user_data["extra"] = extra
     
    return jsonify(user_data), 200

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=80)