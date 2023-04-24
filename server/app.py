from flask import Flask, request, jsonify
 
import sys
import pickle
import json
import numpy as np

__locations = None
__data_columns = None
__model = None


def load_saved_artifacts():
    print("loading saved artifacts...start")
    global  __data_columns
    global __locations

    with open("./artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]  # first 3 columns are sqft, bath, bhk

    global __model
    if __model is None:
        with open('./artifacts/PricePredModel.pickle', 'rb') as f:
            __model = pickle.load(f)
    print("loading saved artifacts...done")


def get_estimated_price(location,sqft,bhk,bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index>=0:
        x[loc_index] = 1

    return round(__model.predict([x])[0],2)




def get_location_name():
    return __locations

def get_data_columns():
    return __data_columns
app = Flask(__name__)

@app.route('/')
def home():
    return "hi"

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    data=get_location_name()
    print(data, file=sys.stderr)
    response = jsonify(
             locations=  get_location_name(),
       
    ) 
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])

    response = jsonify({
        'estimated_price': get_estimated_price(location,total_sqft,bhk,bath)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    load_saved_artifacts()
    print(get_location_name())
    print(get_estimated_price('1st Phase JP Nagar',1000, 3, 3))
    
    app.run()