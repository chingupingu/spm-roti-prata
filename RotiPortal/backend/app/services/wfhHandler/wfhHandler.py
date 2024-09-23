from flask import Flask, request, jsonify
from os import environ
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# @app.route()