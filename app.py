import numpy as np
import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS

application = Flask(__name__)
CORS(application)

# Load the pre-trained SVR models
loaded_fuel_model = joblib.load(open("extra_trees_model.sav", "rb"))
loaded_CO2_model = joblib.load(open("svr_model2.sav", "rb"))

# Load the fitted StandardScaler
loaded_scaler_fuel = joblib.load(open("scaled_data.sav", "rb"))
loaded_scaler_CO2 = joblib.load(open("new_scaled_data.sav", "rb"))

def fuel_prediction(inp):
    arr = np.asarray(inp)
    arr = arr.reshape(1, -1)

    arr_scaled = loaded_scaler_fuel.transform(arr)
    prediction = loaded_fuel_model.predict(arr_scaled)

    return round(prediction[0], 2)

def CO2_prediction(fuel_prediction_result):
    arr = np.asarray([fuel_prediction_result])
    arr = arr.reshape(1, -1)

    arr_scaled = loaded_scaler_CO2.transform(arr)
    prediction = loaded_CO2_model.predict(arr_scaled)

    return round(prediction[0], 2)

def input_converter(inp):
    # vcl = ['Two-seater','Minicompact','Compact','Subcompact','Mid-size','Full-size','SUV: Small','SUV: Standard','Minivan','Station wagon: Small','Station wagon: Mid-size','Pickup truck: Small','Special purpose vehicle','Pickup truck: Standard']
    # trans = ['AV','AM','M','AS','A']
    # fuel = ["D","E","X","Z"]
    # lst = []

    lst = inp

    arr = np.asarray(lst)
    print(lst)

    arr = arr.reshape(1, -1)

    arr_scaled = loaded_scaler_fuel.transform(arr)

    fuel_prediction_result = loaded_fuel_model.predict(arr_scaled)
    CO2_prediction_result = CO2_prediction(fuel_prediction_result)

    return round(fuel_prediction_result[0], 2), CO2_prediction_result

# user_input = [vehicle_class, engine_size, cylinders, transmission, CO2_rating, fuel_type]
# user_input = ["Two Seater", 1.0, 5 , "AM", 6.0, "D"]

@application.route("/", methods=['GET'])
def index():
    return "hello"


@application.route("/get-results/", methods=['GET'])
def get_results():

    vehicleClass = request.args.get("vehicleClass")
    engineSize = request.args.get("engineSize")
    cylinders = request.args.get("cylinders")
    transmission = request.args.get("transmission")
    CO2Rating = request.args.get("CO2Rating")
    D = request.args.get("D")
    E = request.args.get("E")
    X = request.args.get("X")
    Z = request.args.get("Z")

    user_input = [ int(vehicleClass), float(engineSize), float(cylinders) , float(transmission), float(CO2Rating), int(D), int(E), int(X), int(Z)]
    fuel_result, CO2_result = input_converter(user_input)

    results = {
        "id": 0,
        "fuel_result": fuel_result,
        "CO2_result": CO2_result,
    }

    response = jsonify(results)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
   application.run()
