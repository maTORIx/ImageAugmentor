import os
import shutil
import glob

ALLOW_EXTS = ['.png', '.PNG', '.jpg', '.jpeg', '.JPG', '.JPEG', '.bmp', '.BMP']
filter_ext = lambda p:os.path.splitext(p)[-1] in ALLOW_EXTS
slice_label = lambda p:os.path.basename(os.path.dirname(p))

def parse(target, savedir):
    print(os.listdir(target))
    files = glob.glob(os.path.join(target, "**"), recursive=True)
    images = list(filter(filter_ext, files))
    labels = set(map(slice_label, images))
    size = 0

    for label in labels:
        print(labels)
        os.makedirs(os.path.join(savedir, label))
    for src_path in images:
        size += os.path.getsize(src_path)
        shutil.copy(src_path, os.path.join(savedir, os.path.basename(src_path)))
    return size
