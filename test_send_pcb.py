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

# Define the serial port and baud rate
MAC=0
heater_iv=78
heater_rv=21.4
heater_c=14
LED_c=96.3

send_data = 0
response_data = []  
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
    global  MAC,heater_iv,heater_rv,heater_c, LED_c, send_data, response_data
    # Example: Incrementing the variables for demonstration
    
    MAC+=1
    heater_iv+=1
    heater_rv+=1
    heater_c+=1
    LED_c+=1
    

def read_serial_data():
    while True:
        change_send_data()
        if send_data != 2:
            update_variables()  # Update variables when not sending data
        time.sleep(1)

@app.route('/get_data_pcb', methods=['GET'])
def get_data():
    global send_data
    if send_data == 2:
        response_data = {
            "send_data": send_data,
            "MAC_adress": MAC,
            "Heater_IV": heater_iv,
            "Heater_RV": heater_rv,
            "Heater_C": heater_c,
            "LED_C": LED_c
        }
        # Reset send_data after sending values
        return jsonify(response_data)
    else:
        return str(send_data)
    
@app.route('/store_data_pcb', methods=['POST'])
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
    MAC=data.get('MAC_adress')
    heater_iv=data.get('Heater_IV')
    heater_rv=data.get('Heater_RV')
    heater_c=data.get('Heater_C')
    LED_c=data.get('LED_C')

    # Create a dictionary to store in Firestore
    data_to_store = {
        "MAC_adress": MAC,
        "Heater_IV": heater_iv,
        "Heater_RV": heater_rv,
        "Heater_C": heater_c,
        "LED_C": LED_c
    }

    # Store data in Firebase with the incremented ID
    db.collection('values_new_3').document(str(next_id)).set(data_to_store)

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
    app.run(host='0.0.0.0', port=5002)  # Change host and port as needed