import numpy as np
from flask import Flask, request, render_template

app = Flask(__name__,template_folder="templates")
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "0ysh1vzvNqcAbj-w1I4B_r09o9KyC3N-_bd-pYchAsy0"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['GET'])
def predict():
    
    gender = request.args.get('gender')
    stream = request.args.get('stream')
    internship = request.args.get('internship')
    cgpa = request.args.get('cgpa')
    backlogs = request.args.get('backlogs')
    arr = np.array([gender,stream,internship,cgpa,backlogs])
    brr = np.asarray(arr, dtype=float)
    brr_list = brr.tolist()


    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields":['gender','stream','internship','cgpa','backlogs'], "values":[brr_list ]}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/c83b6e01-f939-48e8-92d5-91f6c4372a54/predictions?version=2021-05-01', json=payload_scoring,
        headers={'Authorization': 'Bearer ' + mltoken})
    predictions = response_scoring.json()

    
    predictions = response_scoring.json()
    output=predictions['predictions'][0]['values'][0][0]
    print("Final Prediction", output)

    if(output==1):
        out = 'Placed!!!'
    else:
        out = 'Not Placed!!! Work hard.......'
    return render_template('out.html', output=out)
    print("Final Prediction", output)

if __name__ == "__main__":
    app.run(debug=True)


