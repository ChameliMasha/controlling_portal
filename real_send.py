import serial
from flask import Flask, jsonify
import time
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import request
import threading

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
uid=""
ii=0  
ci=0
cv=0
di=0
dv=0
LED_status = ""   
send_data = 0
response_data = []

@app.route('/get_data', methods=['GET'])
def get_data():
    global uid, cv, ci, dv, di, ii, LED_status, send_data, response_data
    # send_data = 2
    if send_data == 2:
        response_data = {
            "send_data": send_data,
            "UID": uid,
            "II": ii,
            "CI": ci,
            "CV": cv,
            "DI": di,
            "DV": dv,
            "LED_status": LED_status
        }
        send_data = 0  # Reset send_data after sending values
        return jsonify(response_data)
    else:
        return str(send_data)

    
@app.route('/store_data', methods=['POST'])
def store_data():
    print("comes here")
    data = request.json
    # print(data)

    # Get the current ID or initialize if it doesn't exist
    counter_doc = counter_ref.get()
    if not counter_doc.exists:
        counter_ref.set({'current_id': 0})  # Initializing with ID 0
        counter_doc = counter_ref.get()

    counter = counter_doc.to_dict()
    current_id = counter['current_id']
    next_id = current_id + 1

    # Access inDIvidual attributes from the JSON data
    uid = data.get('UID')
    ii = data.get('II')
    ci = data.get('CI')
    cv = data.get('CV')
    di = data.get('DI')
    dv = data.get('DV')
    LED_status = data.get('LED_status')
    print("value of UID in the server:", uid)
    # Create a DIctionary to store in Firestore
    data_to_store = {
        "UID": uid,
        "II": ii,
        "CI": ci,
        "CV": cv,
        "DI": di,
        "DV": dv,
        "LED_status": LED_status
    }

    # Store data in Firebase with the incremented ID
    db.collection('values_new_2').document(str(next_id)).set(data_to_store)

    # Update the counter for the next ID
    counter_ref.set({'current_id': next_id})

    return 'Data stored successfully', 200
    

ser = serial.Serial('COM3', 9600)  # Update 'COM1' with your speCIfic port and 9600 with your baud rate
def read_serial_data(serial_port):
    # print("comes here")
    global uid, cv, ci, dv, di, ii, LED_status, send_data, response_data

    global send_data, response_data
    try:
        while True:
            # Read a line from the serial port
            # print(f"this is serail data:{serial_port.readline()} ")
            line = serial_port.readline().decode('utf-8').strip()
            
            # Print the received data
            print(f"Received: {line}")
            # print(send_data)
            # Read a line from the serial port
            line = ser.readline().decode('utf-8').strip()
        
            # Print the received data
            print(f"Received: {line}")
            # print(send_data)
            parts = line.split(':')
            label = parts[0].strip()
            value = parts[1].strip()
           # print(label)
           # print(value)
            if(label =="uid"):
                uid = value
                print(f"UID:{uid}")
            elif(label == "cv"):
                cv=float(value)
                print(f"CV:{cv}")
            elif(label=="ci"):
                ci =float(value)
                print(f"CI:{ci}")
            elif(label=="dv"):
                dv =float(value)
                print(f"DV:{dv}")
            elif(label=="di"):
                di =float(value)
                print(f"DI:{di}")
            elif(label=="iv"):
                iv=float(value)
                print(f"IV:{iv}")
            elif(label=="ii"):
                ii =float(value)
                print(f"II:{ii}")
            elif(label=="show"):
                send_data = 2
                print("gg")
                # print(send_data)
            elif(label=="start"):
                send_data = 1
                print("start")

            # print(response_data)

    finally:
        # Close the serial port when the loop is terminated
        serial_port.close()
        print("Serial port closed.")

def main():
    # Define the serial port and baud rate
    

    # Start a thread for reading serial data
    # serial_thread = threading.Thread(target=read_serial_data)
    # serial_thread.daemon = True
    # serial_thread.start()

     

    # Run the Flask app
    
    
    try:
        read_serial_data(ser)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure the serial port is closed even in case of an exception
        ser.close()

if __name__ == "__main__":

    serial_thread = threading.Thread(target=main)
    serial_thread.start()

    app.run(host='0.0.0.0', port=5000)
    # main()
     