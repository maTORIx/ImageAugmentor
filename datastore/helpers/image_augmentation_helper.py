import os
import glob
import numpy as np
import numba
import psutil
from PIL import Image

SUPPORTED_EXTENSIONS = [".png", ".PNG", ".jpg", ".jpeg", ".JPG", ".JPEG", ".bmp", ".BMP"]
filter_pathes = lambda n:os.path.splitext(n)[-1] not in SUPPORTED_EXTENSIONS

@numba.jit
def classification(target_dir, save_dir, func, params, batch_size=10):
    classes = os.listdir(target_dir)
    pathes = glob.glob(os.path.join(classes, "*", "*.*"))
    image_pathes = filter(filter_pathes, pathes)
    for i in range(int(len(image_pathes) / batch_size))):
        target_pathes = image_pathes[i*batch_size:i*batch_size+batch_size]
        target_images = [None] * batch_size
        for i, path in enumerate(target_pathes):
            img = Image.open(target_pathes)
            target_images[i] = np.asarray(img)
            img.close()
        result_images = func(target_images)[0]

    
