import os
import json
import uuid
import shutil
import subprocess

from bottle import Bottle, HTTPResponse
from bottle import request, response

app = Bottle()

DATASTORE = "./datastore"

AUGMENT_CHOISES = subprocess.check_output(["python", "COMMAND/image-augmentor.py",  "list", "--json"])
ALLOW_DATASET_EXT = [".zip", ".ZIP", ".tar.gz", ".tar"]

@app.route("/datasets")
def list_datasets():
    tmp = {
        "id": "abeee",
        "name": "sample",
        "type": "classification",
        "size": "400MB",
        "sample_images": [
            "/static/sample.png",
            "/static/sample.png",
            "/static/sample.png"
        ],
        "processing": False
    }
    return json.dumps([tmp])

@app.route("/datasets", method="POST")
def post_dataset():
    uid = uuid.uuid4()
    file = request.files.file
    data_type = request.forms.data_type
    name = request.forms.get("name", file.name)

    if os.path.splitext(file.name)[-1] not in ALLOW_DATASET_EXT:
        return HTTPResponse(status=400)
    
    tmp_dir = os.path.join(DATASTORE, "tmp", uid)
    save_dir = os.path.join(DATASTORE, "datas", uid)
    os.makedirs(tmp_dir)
    os.makedirs(save_dir)

    file.save(os.path.join(tmp_dir, "data{}".format(os.path.splitext(file.name)[-1])))

    return HTTPResponse(
        body=json.dumps({
            "uid": uid
        }),
        status=202
    )

@app.route("/results")
def list_results():
    return json.dumps([{
        "id": "abcde",
        "name": "TIME",
        "type": "classification",
        "size": "400MB",
        "augmentation_option": {},
        "progress": 80,
        "status": "finished"
    }])

@app.route("/augment/option_choises")
def list_augment_choises():
    return AUGMENT_CHOISES