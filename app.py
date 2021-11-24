from flask import Flask ,render_template ,request ,jsonify 
import numpy as np
import joblib 
import sys
import os


app = Flask(__name__) 
inputs = np.zeros(shape = [1,9])


LOCATION = 'OneDrive\Bureau\plentina\model'
model_path = os.path.join(LOCATION, 'model.pkl')
scaler_path = os.path.join(LOCATION, 'scaler.pkl')

model  = joblib.load(model_path)
scaler = joblib.load(scaler_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prediction' , methods = ['POST'])
def greeting():

    inputs[0,0] = float(request.form.get("step"))
    inputs[0,1] = float(request.form.get("type"))
    inputs[0,2] = float(request.form.get("amount"))
    inputs[0,3] = float(request.form.get("oldbalanceOrig"))
    inputs[0,4] = float(request.form.get("newbalanceOrig"))
    inputs[0,5] = float(request.form.get("oldbalanceDest"))
    inputs[0,6] = float(request.form.get("newbalanceDest"))

    if inputs[0,5] == 0 and inputs[0,6] == 0: 
        inputs[0,5] , inputs[0,6] = -1 , -1 

    inputs[0,7] = inputs[0,4] + inputs[0,2] - inputs[0,3]
    inputs[0,8] = inputs[0,5] + inputs[0,2] - inputs[0,6]
    
    X_test = scaler.transform(inputs)

    # json_ = jsonify(X_test.tolist())

    predicted = model.predict(X_test)

    if predicted == [1] :
        a = "scam"
    else : a = 'legit'

    return render_template('prediction.html', a = jsonify({"data": X_test.tolist()}) , b = a )

if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except Exception as e:
        port = 80

    app.run(host='0.0.0.0', port=port, debug=True)