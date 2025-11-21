from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_cors import CORS
from src.main.routes.duepay_route import duepay_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(duepay_bp)