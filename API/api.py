import json

from bottle import Bottle, run
from bottle import template, static_file

app = Bottle()

DATASTORE_PATH = "./datastore"

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
        ]
    }
    return json.dumps([tmp])

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
    return json.dumps({
        "flip-vertical": {
            "name": "flip-vertical",
            "sample_images": {
                "before": "/static/sample.png",
                "after": "/static/sample.png"
            },
            "params": [{
                "name": "random",
                "type": "select",
                "choises": ["true", "false"],
                "default": "false"
            }]
        },
        "flip-horizontal": {
            "name": "flip-horizontal",
            "sample_images": {
                "before": "/static/sample.png",
                "after": "/static/sample.png"
            },
            "params": [
                {
                    "name": "random",
                    "type": "select",
                    "choises": ["true", "false"],
                    "default": "false"
                },
                {
                    "name": "exec_percentage",
                    "type": "number",
                    "unit": "%",
                    "min": 0,
                    "max": 100,
                    "step": 0.1,
                    "min_default": 100,
                }
            ]
        },
        "crop": {
            "name": 'crop',
            "sample_images": {
                "before": "/static/sample.png",
                "after": "/static/sample.png"
            },
            "params": [
                {
                    "name": "top",
                    "type": "range",
                    "unit": "%",
                    "min": 0,
                    "max": 100,
                    "step": 0.1,
                    "min_default": 0,
                    "max_default": 100,
                },
                {
                    "name": "bottom",
                    "type": "range",
                    "unit": "%",
                    "min": 0,
                    "max": 100,
                    "step": 0.1,
                    "min_default": 0,
                    "max_default": 100,
                },
                {
                    "name": "left",
                    "type": "range",
                    "unit": "%",
                    "min": 0,
                    "max": 100,
                    "step": 0.1,
                    "min_default": 0,
                    "max_default": 100,
                },
                {
                    "name": "right",
                    "type": "range",
                    "unit": "%",
                    "min": 0,
                    "max": 100,
                    "step": 0.1,
                    "min_default": 0,
                    "max_default": 100,
                },
                {
                    "name": "select",
                    "type": "select",
                    "choises": ["hello", "world"],
                    "default": "hello"
                }
            ]
        }
    })