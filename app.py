from src import app
import os
from dotenv import load_dotenv, find_dotenv
#basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(find_dotenv())
#load_dotenv(os.path.join(basedir, '.env'))

if __name__ == '__main__':
    app.run(debug=True)