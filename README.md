# transactions
using flask to build an API for sklearn model 

## Flask API for scikit learn
A simple Flask application that can serve predictions from a scikit-learn model.
Reads a pickled sklearn model into memory when the Flask app is started and returns predictions through the /predict endpoint.
You can also use the /train endpoint to train/retrain the model. Any sklearn model can be used for prediction.

*PLEASE change the variable LOCATION to the convenient PATH* 
```
python app.py <port>
```

