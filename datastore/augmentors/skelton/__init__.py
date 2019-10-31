import glob
from datastore.helpers import image_augmentation_helper as ia_helper

def main(target_dir, save_dir, data_type, params):
    return ia_helper.image_augmentation(target_dir, save_dir, data_type, augment, params, batch_size=10)

def augment(batch_images, pair_images=[], keypoints=[]):
    return batch_images, pair_images, keypoints