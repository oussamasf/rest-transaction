from flask import Flask , jsonify
from flask_restful import Resource ,Api ,reqparse
import numpy as np
import joblib 

TYPE_ = ['PAYMENT', 'TRANSFER', 'CASH_OUT', 'DEBIT', 'CASH_IN']

# init flask app and the api 
app = Flask(__name__)
api = Api(app)

# importing serialized sklearn models 
model  = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')

class Transactions (Resource):

    def post (self) : 
        inputs = np.zeros(shape = [1,9])

        # init the parser 
        parser = reqparse.RequestParser()

        # adding arguments 
        parser.add_argument('step' , required = True)
        parser.add_argument('type' , required = True)
        parser.add_argument('amount' , required = True)
        parser.add_argument('nameOrig' , required = False)
        parser.add_argument('oldbalanceOrig' , required = True)
        parser.add_argument('newbalanceOrig' , required = True)
        parser.add_argument('nameDest' , required = False)
        parser.add_argument('oldbalanceDest' , required = True)
        parser.add_argument('newbalanceDest' , required = True)

        # convert it to a dict 
        arg = parser.parse_args()

        # encoding type param
        if (arg['type']== TYPE_[0] or
            arg['type']== TYPE_[3] or
            arg['type']== TYPE_[4]) :

            return jsonify({'isFraud':False})

        elif arg['type']== TYPE_[1] : 

            inputs[0,1] = float(0)

        else : 

            inputs[0,1] = float(1)

        # handling not valid inputs 
        try : 
            inputs[0,0] = float(arg["step"])
            inputs[0,2] = float(arg["amount"])
            inputs[0,3] = float(arg["oldbalanceOrig"])
            inputs[0,4] = float(arg["newbalanceOrig"])
            inputs[0,5] = float(arg["oldbalanceDest"])
            inputs[0,6] = float(arg["newbalanceDest"])

        except : 
            return jsonify({'message':'not valid'}) , 422


        # calculation ' putting the model into production '
        if inputs[0,5] == 0 and inputs[0,6] == 0: 
            inputs[0,5] , inputs[0,6] = -1 , -1 

        inputs[0,7] = inputs[0,4] + inputs[0,2] - inputs[0,3]
        inputs[0,8] = inputs[0,5] + inputs[0,2] - inputs[0,6]
        
        X_test = scaler.transform(inputs)
        predicted = model.predict(X_test)

        if predicted == [1] :
            return jsonify({'isFraud' : True })
        else : 
            return jsonify({'isFraud' : False })


    def get (self):
        return jsonify({'message':"please check documentation to use this API"}) 
     

api.add_resource(Transactions,'/')

if __name__ == '__main__' : 
    app.run()