from flask import Flask, jsonify
import time
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import request

# Initialize Firebase Admin SDK with your service account credentials
cred = credentials.Certificate('private_key.json')
firebase_admin.initialize_app(cred)

# Access Firestore database
db = firestore.client()

# Counter to maintain ascending IDs
counter_ref = db.collection('counters').document('data_counter')

app = Flask(__name__)
CORS(app)

# Your global variables
UID = 45.2
DV = 32.5
DI = 85.2
IV = 412
CV = 96.5
II = 23.4
CI = 58.2
LED_status = ""

send_data = 0
label = 0

def change_send_data():
    global send_data, label
    if label == 1:
        send_data = 1
    elif label == 10:
        send_data = 2
        # time.sleep(20)
    label = (label + 1) % 11  # Reset label after 10 counts

def update_variables():
    global UID, DV, DI, IV, CV, II, CI
    # Example: Incrementing the variables for demonstration
    UID += 1
    DV += 1
    DI += 1
    IV += 1
    CV += 1
    II += 1
    CI += 1

def read_serial_data():
    while True:
        change_send_data()
        if send_data != 2:
            update_variables()  # Update variables when not sending data
        time.sleep(1)

@app.route('/get_data', methods=['GET'])
def get_data():
    global send_data
    print(send_data)
    print(UID)
    if send_data == 2:
        response_data = {
            "send_data": send_data,
            "UID": UID,
            "DV": DV,
            "DI": DI,
            "IV": IV,
            "CV": CV,
            "II": II,
            "CI": CI,
            "LED_status": LED_status
        }
        # Reset send_data after sending values
        return jsonify(response_data)
    else:
        return str(send_data)
    
@app.route('/store_data', methods=['POST'])
def store_data():
    print("comes here")
    data = request.json
    print(data)

    # Get the current ID or initialize if it doesn't exist
    counter_doc = counter_ref.get()
    if not counter_doc.exists:
        counter_ref.set({'current_id': 0})  # Initializing with ID 0
        counter_doc = counter_ref.get()

    counter = counter_doc.to_dict()
    current_id = counter['current_id']
    next_id = current_id + 1

    # Access individual attributes from the JSON data
    UID = data.get('UID')
    DV = data.get('DV')
    DI = data.get('DI')
    IV = data.get('IV')
    CV = data.get('CV')
    II = data.get('II')
    CI = data.get('CI')
    LED_status = data.get('LED_status')

    # Create a dictionary to store in Firestore
    data_to_store = {
        "UID": UID,
        "DV": DV,
        "DI": DI,
        "IV": IV,
        "CV": CV,
        "II": II,
        "CI": CI,
        "LED_status": LED_status
    }

    # Store data in Firebase with the incremented ID
    db.collection('values_new_2').document(str(next_id)).set(data_to_store)

    # Update the counter for the next ID
    counter_ref.set({'current_id': next_id})

    return 'Data stored successfully', 200

if __name__ == "__main__":
    import threading

    # Start a thread for reading serial data
    serial_thread = threading.Thread(target=read_serial_data)
    serial_thread.daemon = True
    serial_thread.start()

    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)  # Change host and port as needed