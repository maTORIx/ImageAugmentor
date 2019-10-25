from bottle import Bottle, run
from bottle import template, static_file

app = Bottle()
STATIC_FILES_DIR = './ui/static'

# with open("./ui/templates/index.html") as f:
#     index_html = f.read()

@app.route("/")
def index():
    with open("./ui/templates/index.html") as f:
        index_html = f.read()
    return index_html

@app.route('/static/<file_path:path>')
def static_files(file_path):
    return static_file(file_path, STATIC_FILES_DIR)
