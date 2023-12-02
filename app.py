from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/start', methods=['POST'])
def handle_start():
    print("Loading..")
    return "Loading.."

@app.route('/show', methods=['GET'])
def handle_request():
    # Retrieving the query parameters sent with the request
    key1 = request.args.get('key1')
    key2 = request.args.get('key2')

    # Do whatever you need with the retrieved parameters
    result = {"key1": key1, "key2": key2}
    
    # Writing the result to a separate file
    print(key1)
    print(key2)
    
    return result

if __name__ == '__main__':
    app.run(debug=True, port=8080)
