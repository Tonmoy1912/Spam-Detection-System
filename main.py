from flask import Flask, send_from_directory,jsonify, request, json
from flask_cors import CORS
import os
import pickle
import re

app = Flask(__name__, static_folder='frontend/dist')
CORS(app)  # Enable CORS for all routes

model_path = 'model.pkl'
vectorizer_path='vectorizer.pkl'
all_stopwords_path='all_stopwords.pkl'
ps_path='ps.pkl'
with open(model_path, 'rb') as file:
    model = pickle.load(file)
with open(vectorizer_path, 'rb') as file:
    vectorizer = pickle.load(file)
with open(all_stopwords_path, 'rb') as file:
    all_stopwords = pickle.load(file)
with open(ps_path, 'rb') as file:
    ps = pickle.load(file)


def get_prediction_result(msg):
    msg = re.sub('[^a-zA-Z]', ' ', msg)
    msg = msg.lower()
    msg = msg.split()
    msg = [ps.stem(word) for word in msg if not word in set(all_stopwords)]
    msg = ' '.join(msg)
    # print(msg)
    input_data=vectorizer.transform([msg]).toarray()
    # print(input_data)
    result=model.predict(input_data)
    # print(result)
    if result[0]==0:
        result="ham"
    else:
        result="spam"
    return  result
    # print(result)

# Serve React static files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    print(path)
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


# Example API route
@app.route('/test', methods=['GET'])
def get_data():
    data={
        "message":"Healty Server",
        "ok":True
    }
    return data

@app.route('/predict', methods=['POST'])
def predict():
    body=json.loads(request.data)
    # print(body)
    result=get_prediction_result(body['message'])
    # print(result)
    return {"result":result}
    # return {"result":"ham"}
    # return {"result":"spam"}

if __name__=="__main__":
    app.run(debug=True,port=8000)