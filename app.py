import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
from flask import Flask, request, jsonify

application = Flask(__name__)

# Load the pre-trained SVR models
loaded_fuel_model = joblib.load(open("svr_model.sav", "rb"))
loaded_CO2_model = joblib.load(open("svr2_model.sav", "rb"))

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
    vcl = ['Two-seater','Minicompact','Compact','Subcompact','Mid-size','Full-size','SUV: Small','SUV: Standard','Minivan','Station wagon: Small','Station wagon: Mid-size','Pickup truck: Small','Special purpose vehicle','Pickup truck: Standard']
    trans = ['AV','AM','M','AS','A']
    fuel = ["D","E","X","Z"]
    lst = []

    for i in range(6):
        if isinstance(inp[i], str):
            if inp[i] in vcl:
                lst.append(vcl.index(inp[i]))
            elif inp[i] in trans:
                lst.append(trans.index(inp[i]))
            elif inp[i] in fuel:
                if fuel.index(inp[i]) == 0:
                    lst.extend([1, 0, 0, 0])
                    break
                elif fuel.index(inp[i]) == 1:
                    lst.extend([0, 1, 0, 0])
                    break
                elif fuel.index(inp[i]) == 2:
                    lst.extend([0, 0, 1, 0])
                    break
                elif fuel.index(inp[i]) == 3:
                    lst.extend([0, 0, 0, 1])
        else:
            lst.append(inp[i])

    arr = np.asarray(lst)
    arr = arr.reshape(1, -1)

    arr_scaled = loaded_scaler_fuel.transform(arr)

    fuel_prediction_result = loaded_fuel_model.predict(arr_scaled)
    CO2_prediction_result = CO2_prediction(fuel_prediction_result)

    return round(fuel_prediction_result[0], 2), CO2_prediction_result

# user_input = [vehicle_class, engine_size, cylinders, transmission, CO2_rating, fuel_type]
user_input = ["Two Seater", 1.0, 5 , "AM", 6.0, "D"]

@application.route("/")
def index():
    return "hello"


@application.route("/get-results/")
def get_results():
    
    fuel_result, CO2_result = input_converter(user_input)

    results = {
        "id": 0,
        "fuel_result": fuel_result,
        "CO2_result": CO2_result,
    }

    # extra = request.args.get("extra")

    # if extra:
    #     results["extra"] = extra
    
    return jsonify(results), 200

if __name__ == "__main__":
   application.run()
