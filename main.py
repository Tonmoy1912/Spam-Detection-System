from flask import Flask, send_from_directory,jsonify, request, json
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='frontend/dist')
CORS(app)  # Enable CORS for all routes

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
    print(body)
    return {"result":"ham"}
    # return {"result":"spam"}

if __name__=="__main__":
    app.run(debug=True,port=8000)