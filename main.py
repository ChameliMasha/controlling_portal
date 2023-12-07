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

# Your global variables for the first server
