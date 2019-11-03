import os
import argparse
from bottle import run, static_file

from UI import ui
from API import api

app = ui.app
app.mount("/api", api.app)

DATASTORE_DIR = "./datastore"
@app.route('/datastore/<file_path:path>')
def static_files(file_path):
    return static_file(file_path, DATASTORE_DIR)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=8000)
    
    args = parser.parse_args()
    run(app=app, host=args.host, port=args.port, debug=True ,reloader=True)

if __name__ == '__main__':
    main()
