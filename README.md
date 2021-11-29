# transactions
using flask to build an API for sklearn model 

## Flask API for scikit learn
A simple Flask application that can serve predictions from a scikit-learn model.
Reads a pickled sklearn model into memory when the Flask app is started and returns predictions through the /predict endpoint.
Any sklearn model can be used for prediction.

```
python app.py <port>
```

