from flask import Flask
from flask_cors import CORS
from google.cloud import firestore

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    app.config.from_object('app.config.Config')
    
    # Initialize Firestore
    app.firestore_client = firestore.Client()

    with app.app_context():
        from .routes import register_routes
        register_routes(app)
    
    return app