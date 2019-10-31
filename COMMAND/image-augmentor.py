import os
import json
import glob
import argparse
import zipfile
import datetime
import importlib
import numba

from status import Status

DATASTORE_DIR = os.path.join(os.path.dirname(__file__), "..", "datastore")
AUGMENTORS_DIR = os.path.join(DATASTORE_DIR, "augmentors")
DATATYPE_DIR = os.path.join(DATASTORE_DIR, "data_types")
SAMPLE_IMAGE_URL = "/static/noimage.png"
STATUS_WRITE_SPAN_SEC = 3

def set_parser():
    parser = argparse.ArgumentParser(description="ImageAugmentor")
    subparsers = parser.add_subparsers()
    
    parser_exec = subparsers.add_parser('exec', help='execute augmentation')
    parser_exec.add_argument("--json", type=str, help="select json for set params")
    parser_exec.add_argument("-O", action="store_true", help="input json from pipe")
    parser_exec.set_defaults(handler=command_exec)

    parser_parse = subparsers.add_parser("parse", help="parse data as data_type")
    parser_parse.add_argument("data_type", type=str, help="data_type")
    parser_parse.add_argument("target", type=str, help="parse target file or directory")
    parser_parse.add_argument("savedir", type=str, help="save result directory")
    parser_parse.add_argument("--statusfile", type=str, help="write status with json")
    parser_parse.set_defaults(handler=command_parse)

    parser_list = subparsers.add_parser('list', help='list executable augmentors')
    parser_list.add_argument("--json", action="store_true", help="export as json")
    parser_list.set_defaults(handler=command_list)

    return parser

def command_exec(args):
    print(args)

def command_parse(args):
    data_types = list_data_types()
    if args.data_type not in data_types:
        raise ValueError("Invalid data_type")
    elif not os.path.exists(args.target):
        raise ValueError("Invalid target. {} does not exist.".format(args.target))
    elif os.path.exists(args.savedir):
        raise ValueError("Invalid savedir. {} already exists.".format(args.savedir))

    os.makedirs(args.savedir)
    status = Status(args.statusfile)
    if os.path.splitext(args.target)[-1] in [".zip", ".ZIP"]:
        status.update_msg("decompressing")
        extract_dir = os.path.join(args.savedir, ".tmp")
        os.makedirs(extract_dir)
        with zipfile.ZipFile(args.target) as f:
            f.extractall(extract_dir)
        args.target = extract_dir
    status.update_msg("parsing")

    loader = importlib.machinery.SourceFileLoader(args.data_type, os.path.join(DATATYPE_DIR, args.data_type, '__init__.py'))
    parser = loader.load_module()

    size = parser.parse(os.path.abspath(args.target), os.path.abspath(args.savedir))
    if size == None:
        size = get_directory_size(args.savedir)
    status.finish()
    print(size)

def command_list(args):
    settings = load_augmentor_settings()
    
    if args.json:
        print(json.dumps(settings, indent=2))
        return
    for key in settings:
        print("- {}".format(settings[key]["name"]))
        print("    data_types:")
        for data_type in settings[key]["data_types"]:
            print("      - " + data_type)
        print("    params:")
        for param in settings[key]["params"]:
            print("      - " + param["name"])
            for conf_key in param:
                if conf_key == 'name':
                    continue
                elif type(param[conf_key]) == list:
                    print("          {}:".format(conf_key))
                    for item in param[conf_key]:
                        print("            - {}".format(item))
                else:
                    print("          {}: {}".format(conf_key, param[conf_key]))

def list_data_types():
    return list(filter(lambda p:os.path.isdir(os.path.join(DATATYPE_DIR, p)), os.listdir(DATATYPE_DIR)))

def list_augmentors():
    return  list(filter(lambda p:os.path.isdir(os.path.join(AUGMENTORS_DIR, p)), os.listdir(AUGMENTORS_DIR)))

def load_augmentor_settings():
    settings = {}
    for augmentor in list_augmentors():
        if not os.path.isdir(os.path.join(AUGMENTORS_DIR, augmentor)):
            continue
        with open(os.path.join(AUGMENTORS_DIR, augmentor, "args.json")) as f:
            settings[augmentor] = json.load(f)
    return settings

def get_directory_size(directory_path):
    size = 0
    files = filter(lambda p:os.path.isfile(p), glob.glob(os.path.join(directory_path, "**"), recursive=True))
    return sum([os.path.getsize(p) for p in list(files)])

def main():
    parser = set_parser()
    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()