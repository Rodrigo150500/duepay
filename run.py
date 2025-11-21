import os
from src.main.server.server import app

PORT = os.getenv("PORT")
HOST = os.getenv("HOST")

if __name__ == "__main__":
    app.run(debug=True, port=PORT, host=HOST)