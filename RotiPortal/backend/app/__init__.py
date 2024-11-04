import os
from flask import Flask
from flask_cors import CORS
from firebase_admin import credentials, initialize_app, firestore
from google.oauth2 import service_account
from dotenv import load_dotenv
firebase_initialized = False

def create_app(service_account_json):
    global firebase_initialized
    # Load environment variables from .env
    load_dotenv()

    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    app.config.from_object('app.config.Config')

    if service_account_json is None:
        if not firebase_initialized:
            # Use the credentials from the environment variable
            cred = credentials.Certificate(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
            initialize_app(cred, {
                "storageBucket": "gs://roti-portal-392216.appspot.com"
            })
            firebase_initialized = True
    else:
        if not firebase_initialized:
            cred = service_account.Credentials.from_service_account_info(service_account_json)
            initialize_app(cred, {
                "storageBucket": "gs://roti-portal-392216.appspot.com"
            })
            firebase_initialized = True

    # Initialize Firestore
    db = firestore.Client()

    # Register routes
    with app.app_context():
        from .routes import register_routes
        register_routes(app)

    # Optionally store the db in the app config or a global variable
    app.config['DB'] = db  # Store db in app config if needed

    return app  # Return only the app object