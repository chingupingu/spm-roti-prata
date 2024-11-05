import os
import json
from flask import Flask
from flask_cors import CORS
from firebase_admin import credentials, initialize_app, firestore, get_app
from google.oauth2 import service_account
from dotenv import load_dotenv
firebase_initialized = False

def create_app():
    global firebase_initialized
    # Load environment variables from .env
    load_dotenv()

    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    app.config.from_object('app.config.Config')

    try:
        get_app()  # This will raise an exception if the app does not exist
    except ValueError:
        # # use this if running locally
        # cred = credentials.Certificate(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
        # initialize_app(cred, {
        #     "storageBucket": "gs://roti-portal-392216.appspot.com"
        # })

        # use this if running on vercel
        cred_json = json.loads(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
        cred = credentials.Certificate(cred_json)
        initialize_app(cred, {
            "storageBucket": "gs://roti-portal-392216.appspot.com"
        })


    # Initialize Firestore
    db = firestore.Client()

    # Register routes
    with app.app_context():
        from .routes import register_routes
        register_routes(app)

    # Optionally store the db in the app config or a global variable
    app.config['DB'] = db  # Store db in app config if needed

    return app  # Return only the app object