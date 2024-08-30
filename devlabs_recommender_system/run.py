from devlabs_recommender_system.api import app
from waitress import serve
from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

def main():
    serve(app, host=HOST, port=PORT)

if __name__ == "__main__":
    main()