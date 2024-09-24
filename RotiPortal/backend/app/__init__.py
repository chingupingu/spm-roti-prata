import os
import json
# from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from firebase_admin import credentials, initialize_app
# from google.cloud import firestore

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    app.config.from_object('app.config.Config')
    
    # Initialize Firestore
    cred = credentials.Certificate({
        "type": "service_account",
        "project_id": "rotiprata-de9d9",
        "private_key_id": "132185ac27f1526f525e8e27c733a66657ef11c0",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDUtv5ro8M5ARzm\n7J5mgOG08fXSG0WCgWi47NbKmjhHVKT9SqE4yUUWij0ph1s5zZ9gOcZLuJbtbGpQ\nIy23wcVGKvIaTx5zLDm7QJA0EwHsBmtX+2i4Bn8JqfCr7XK9mSu7+Ney0kvmtU3a\nSwswMHwuEG7P3Y+RJDtY5Gr4vWm+OWhCI8vM4+BUDIHpDkcNEdc6Jqw/29pvGBHB\n9G9iHD7WckqUVdYGA4ou4KceOC+6WxONAKAjkYISK0Mpo/As4FiSp8ExkYQ5nm7Q\nB6QdPSJtEtJ3TdFOLpm2L0IwfFunMbyFQY6eMtAkLg4BGrtJ6tWuc+8iMEC56SMw\nRmWZ8JdVAgMBAAECggEAMJmMwJAecwA/l705JadNqldb+EC13W7uu82U955LvHRo\n69wowL4vlEpKVhowbCEASG560WMfzKgoFB4tfF3/0hvOy9cG2H6ixBcou1Uaa9A9\np1DwKJeHX/BdZhKu1AXSebSNp7QnllMXMghSSpTRUn77qm9vNVSnYJRzolg4eDbf\n2ojRciICoY/f9qyfghtyv0Uo+lGDuBwdVe7Gz5SAc3W3R3fjxM3hBRnhRXbj2s+I\nYrNt4WsU99rYIDSX6KVt55WDNtGusEAq+3h4KWx/VGYLd+4EF0enSA6dIL+vO4T1\nPFwIy0S9jBXIJAmuTVJMLnsTkqVhrM/7mjEJfmMBgQKBgQDxgmJVTZEByGa3//OX\nlKrZK4d7UlkFtfoinhrPYrFB/0qg/6WGIX+7UId23S+0+aF7i1ur43mEoH5Gauch\nKQGxKAqybECI+rcdU5luRCE0rnZh3McT/9VnuU+Wuo8ydmT6MMXmuocxuWkByMze\nB4pHatyK/EpSYA1UA6v0hB6tFQKBgQDhelKHuSnFwPj/rewEMs9sLtEcGHnCqqxE\nOvjBFSa4JVg41RTJTYEVie8ueFa3xtSafXIqnMsomy585NErSGfC7wNaCukx2rFW\n6XVE4vilHDxXMrbiSBHXJgTlIXiYQchGffA2C2221Zo5icyoTTtjFvSgyW42mVy8\n/R1FupdRQQKBgQDEXfZkU6BO6coTW+qNWlUcJVeQfyFhElji4tj7vMxR1CizBYpp\nqD06abzreeb7aGnTkTklZtz8aJ6j1PI/NR9qExu3fWtvtSNElh/P11eEhUI+SgwY\nh9DV+IftD521MyzhfNy8wPeCB7aIu+NPuKPHc+0EmSQ5HF5Z7G5Zbz+eDQKBgQCG\nFdUQazeBJzGr8oShNooNHoYx/AgkkJRi+uLFB8v/xA2Dtotm7pUt9tnqu5tuLGpv\n+Nu0pYtW+XmawgP1hlhWHwbSPBzTDedZ9PlM3uDYZ0Mm47zIMe2SEUTl8ZKikLQF\n34zCxucWzE2rm9u91jfTxGnzV/YXt/njVW5b8gtcQQKBgChpHP5gCrG8noZA1dTx\nAQFlxqxdILb7EdTBOo7RySL5ibKeJX3p423mwj9b/SG+2QrI4thWsAw1Lx6VM/Zk\nzVbwVbJlVKg4J6SRWDCb21zd0XBPDMJ8tF0fqYuj5Vyr1oOFGWGpgl3mmBJOzqf4\n8e6lzb7wUU0G6TwuOGKijGxo\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-87ppb@rotiprata-de9d9.iam.gserviceaccount.com",
        "client_id": "115053292593092275992",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-87ppb%40rotiprata-de9d9.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
        }
    )
    initialize_app(cred)

    # json_str = os.getenv('SERVICE_ACCT_CREDS')
    # if json_str:
    #     try:
    #         json_data = json.loads(json_str)
    #         cred = credentials.Certificate(json_data)
    #         initialize_app(cred)
    #     except json.JSONDecodeError:
    #         print("Error: Invalid JSON string in environment variable")

    # app.firestore_client = firestore.Client()

    with app.app_context():
        from .routes import register_routes
        register_routes(app)
    
    return app