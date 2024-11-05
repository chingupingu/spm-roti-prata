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

    try:
        get_app()  # This will raise an exception if the app does not exist
    except ValueError:
        # # use this if running locally
        # cred = credentials.Certificate(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
        # initialize_app(cred, {
        #     "storageBucket": "gs://roti-portal-392216.appspot.com"
        # })

        # use this if running on vercel
        google_application_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if google_application_credentials:
            cred_json = json.loads(google_application_credentials)
            # cred = credentials.Certificate(cred_json)
            credentials, project_id = load_credentials_from_dict(cred_json)
            initialize_app(credentials, {
                "storageBucket": "gs://roti-portal-392216.appspot.com"
            })
        else:
            print("Warning: GOOGLE_APPLICATION_CREDENTIALS not found in environment")



    # Initialize Firestore
    # db = firestore.Client()
    db = firestore.Client(project=cred_json.get('project_id'))


    # Register routes
    with app.app_context():
        from .routes import register_routes
        register_routes(app)

    # Optionally store the db in the app config or a global variable
    app.config['DB'] = db  # Store db in app config if needed

    return app  # Return only the app object