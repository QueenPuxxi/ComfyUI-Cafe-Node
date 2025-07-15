import os
import hashlib
import numpy as np
from PIL import Image, ImageOps, ImageSequence
import torch

import folder_paths
import node_helpers


class LoadImg:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]

        return {
            "required": {
                "image": (sorted(files), {"image_upload": True}),
                "keep_alpha_channel": ("BOOLEAN", {"default": False, "label_on": "enabled", "label_off": "disabled"}),
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK", "STRING")
    RETURN_NAMES = ("image", "mask", "filename")
    FUNCTION = "load_image"
    CATEGORY = '输入Input☕️'

    @staticmethod
    def load_image(image, keep_alpha_channel):
        image_path = folder_paths.get_annotated_filepath(image)

        img = node_helpers.pillow(Image.open, image_path)

        output_images = []
        output_masks = []
        w, h = None, None

        excluded_formats = ['MPO']

        for i in ImageSequence.Iterator(img):
            i = node_helpers.pillow(ImageOps.exif_transpose, i)

            if i.mode == 'I':
                i = i.point(lambda pixel: pixel * (1 / 255))

            has_alpha = "A" in i.getbands()
            if has_alpha and keep_alpha_channel:
                image_data = i.convert("RGBA")
            else:
                image_data = i.convert("RGB")

            if len(output_images) == 0:
                w = image_data.size[0]
                h = image_data.size[1]

            if image_data.size[0] != w or image_data.size[1] != h:
                continue

            image_np = np.array(image_data).astype(np.float32) / 255.0
            image_tensor = torch.from_numpy(image_np)[None, ]

            if 'A' in i.getbands():
                mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                mask = 1. - torch.from_numpy(mask)
            else:
                mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")

            output_images.append(image_tensor)
            output_masks.append(mask.unsqueeze(0))

        if len(output_images) > 1 and img.format not in excluded_formats:
            output_image = torch.cat(output_images, dim=0)
            output_mask = torch.cat(output_masks, dim=0)
        else:
            output_image = output_images[0]
            output_mask = output_masks[0]

        filename_no_ext = os.path.splitext(image)[0]  # 去掉扩展名
        return output_image, output_mask, filename_no_ext


    @classmethod
    def IS_CHANGED(cls, image, keep_alpha_channel):
        image_path = folder_paths.get_annotated_filepath(image)
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        return m.digest().hex()

    @classmethod
    def VALIDATE_INPUTS(cls, image, keep_alpha_channel):
        if not folder_paths.exists_annotated_filepath(image):
            return "LoadImg(Light-Tool): Invalid image file: {}".format(image)
        return True