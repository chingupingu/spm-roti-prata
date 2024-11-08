import os
import json
from flask import Flask
from flask_cors import CORS
from firebase_admin import credentials, initialize_app, firestore, get_app
from google.auth import load_credentials_from_dict
from dotenv import load_dotenv
firebase_initialized = False

def create_app():
    global firebase_initialized
    # Load environment variables from .env
    load_dotenv()

    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    app.config.from_object('app.config.Config')

    # try:
    #     get_app()  # This will raise an exception if the app does not exist
    # except ValueError:
    #     # use this if running locally
    #     cred = credentials.Certificate(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
    #     initialize_app(cred, {
    #         "storageBucket": "gs://roti-portal-392216.appspot.com"
    #     })

    # Initialize Firestore
    # db = firestore.Client()

    # use this if running on Render (deployed)
    google_credentials_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if google_credentials_json:
        try:
            # Parse the JSON string from environment variable
            credentials_dict = json.loads(google_credentials_json)
            
            # For Firebase Admin initialization
            firebase_cred = credentials.Certificate(credentials_dict)
            initialize_app(firebase_cred, {
                "storageBucket": "gs://roti-portal-392216.appspot.com"
            })
            
            # For Firestore initialization
            google_cred, project_id = load_credentials_from_dict(credentials_dict)
            db = firestore.Client(
                project=project_id,
                credentials=google_cred
            )
        except Exception as e:
            print(f"Error initializing Firebase: {e}")
            # Initialize a default db to prevent UnboundLocalError
            db = None
    else:
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS not found in environment")
        db = None

    

    # Register routes
    with app.app_context():
        from .routes import register_routes
        register_routes(app)

    # Optionally store the db in the app config or a global variable
    app.config['DB'] = db  # Store db in app config if needed

    return app  # Return only the app object