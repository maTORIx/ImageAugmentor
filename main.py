import os
import argparse
from bottle import run, HTTPResponse

from UI import ui
from API import api

app = ui.app
app.mount("/api", api.app)

AUGMENTORS_DIR = "./augmentors"
ALLOW_ACCESS_EXTS = ['.png', '.PNG', '.jpg', '.jpeg', '.JPG', '.JPEG']
@app.route('/augmentors/<file_path:path>')
def static_files(file_path):
    if ALLOW_ACCESS_EXTS not in os.path.splitext(file_path)[1]:
        return HTTPResponse(status=404)
    return static_file(file_path, AUGMENTORS_DIR)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=8000)
    
    args = parser.parse_args()
    run(app=app, host=args.host, port=args.port, debug=True ,reloader=True)

if __name__ == '__main__':
    main()
