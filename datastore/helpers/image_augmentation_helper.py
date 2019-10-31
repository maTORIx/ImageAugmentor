import os
import glob
import random
import shutil
import uuid
import numpy as np
import numba
from PIL import Image

SUPPORTED_EXTENSIONS = [".png", ".PNG", ".jpg", ".jpeg", ".JPG", ".JPEG", ".bmp", ".BMP"]
filter_ext = lambda n:os.path.splitext(n)[-1] in SUPPORTED_EXTENSIONS
slice_label = lambda n:os.path.basename(os.path.dirname(n))

@numba.jit
def classification(target_dir, save_dir, func, params, batch_size=10):
    labels = os.listdir(target_dir)
    pathes = glob.glob(os.path.join(target_dir, "*", "*.*"))
    image_pathes = list(filter(filter_ext, pathes))
    image_labels = list(map(slice_label, image_pathes))

    exec_count = params.get("number_of_executions", 1)
    include_default = params.get("include_default_images", False)
    ext = params.get("save_ext", "png")
    max_progress = len(image_pathes) * exec_count
    progress = 0

    classification_savedir_setup(save_dir, labels)

    for i in range(int(len(image_pathes) / batch_size))):
        target_pathes = image_pathes[i*batch_size:i*batch_size+batch_size]
        target_labels = image_labels[i*batch_size:i*batch_size+batch_size]
        target_images = [None] * len(target_pathes)
        for j, path in enumerate(target_pathes):
            img = Image.open(target_pathes[j])
            target_images[j] = np.asarray(img)
            img.close()
        if include_default:
            classification_save(target_dir, target_labels, target_images, ext=ext)
        for j in range(exec_count):
            result_images, _, _ = func(batch_images=target_images)[0]
            classification_save(target_dir, image_labels, result_images, ext=ext)
            progress += len(target_pathes)
            yield "{}/{}".format(progress, max_progress)

def classification_savedir_setup(target_dir, labels):
    for label in set(labels):
        os.makedirs(os.path.join(target_dir, label), exist_ok=True)

@numba.jit
def classification_save(target_dir, labels, images, ext="png"):
    for i in range(len(images)):
        filename = "{}.{}".format(uuid.uuid4(), ext)
        savepath = os.path.join(target_dir, labels[i], filename)
        Image.fromarray(images[i]).save(savepath)

def image_augmentation(target_dir, save_dir, data_type, func, params, batch_size):
    if data_type == "image_classification":
        return classification(target_dir, save_dir, func, params, batch_size=batch_size)