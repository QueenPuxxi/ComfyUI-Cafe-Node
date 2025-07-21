import os
import csv
import json
import torch
import numpy as np
from PIL import Image
from PIL.PngImagePlugin import PngInfo

import folder_paths

# ======================== 日志颜色定义与日志函数 ========================
COLORS_FG = {
    'BLACK': '\33[30m',
    'RED': '\33[31m',
    'GREEN': '\33[32m',
    'YELLOW': '\33[33m',
    'BLUE': '\33[34m',
    'MAGENTA': '\33[35m',
    'CYAN': '\33[36m',
    'WHITE': '\33[37m',
    'GREY': '\33[90m',
    'BRIGHT_RED': '\33[91m',
    'BRIGHT_GREEN': '\33[92m',
    'BRIGHT_YELLOW': '\33[93m',
    'BRIGHT_BLUE': '\33[94m',
    'BRIGHT_MAGENTA': '\33[95m',
    'BRIGHT_CYAN': '\33[96m',
    'BRIGHT_WHITE': '\33[97m',
}

COLORS_STYLE = {
    'RESET': '\33[0m',
    'BOLD': '\33[1m',
    'NORMAL': '\33[22m',
    'ITALIC': '\33[3m',
    'UNDERLINE': '\33[4m',
    'BLINK': '\33[5m',
    'BLINK2': '\33[6m',
    'SELECTED': '\33[7m',
}

def _get_log_msg(color, node_name, message=None, prefix=''):
    msg = f'{COLORS_STYLE["BOLD"]}{color}{prefix}{node_name}'
    msg += f':{COLORS_STYLE["RESET"]} {message}' if message is not None else f'{COLORS_STYLE["RESET"]}'
    return msg

def _log_node(color, node_name, message=None, prefix=''):
    print(_get_log_msg(color, node_name, message, prefix=prefix))

def log_node_info(node_name, message=None):
    _log_node(COLORS_FG["CYAN"], node_name, message)

def log_node_warn(node_name, message=None):
    _log_node(COLORS_FG["YELLOW"], node_name, message)
# =======================================================================

class CafeSaveText:

    def __init__(self):
        self.output_dir = folder_paths.output_directory
        self.type = 'output'

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"default": "", "forceInput": True}),
                "output_file_path": ("STRING", {"multiline": False, "default": ""}),
                "file_name": ("STRING", {"multiline": False, "default": ""}),
                "file_extension": (["txt", "csv"],),
                "overwrite": ("BOOLEAN", {"default": True}),
                "number_padding": ("INT", {"default": 4, "min": 1, "max": 10}),
            },
            "optional": {
                "image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("STRING", "IMAGE")
    RETURN_NAMES = ("text", "image")
    FUNCTION = "save_text"
    OUTPUT_NODE = True
    CATEGORY = "保存输出☕️"

    def save_image(self, images, filename_prefix, extension='png', quality=100, prompt=None,
                   extra_pnginfo=None, delimiter='_', number_padding=4, output_path='',
                   embed_workflow='true', lossless_webp=False):

        for image in images:
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

            if extension == 'webp':
                img_exif = img.getexif()
                workflow_metadata = ''
                if prompt is not None:
                    img_exif[0x010f] = "Prompt:" + json.dumps(prompt)
                if extra_pnginfo is not None:
                    for x in extra_pnginfo:
                        workflow_metadata += json.dumps(extra_pnginfo[x])
                img_exif[0x010e] = "Workflow:" + workflow_metadata
                exif_data = img_exif.tobytes()
            else:
                metadata = PngInfo()
                if embed_workflow == 'true':
                    if prompt is not None:
                        metadata.add_text("prompt", json.dumps(prompt))
                    if extra_pnginfo is not None:
                        for x in extra_pnginfo:
                            metadata.add_text(x, json.dumps(extra_pnginfo[x]))
                exif_data = metadata

            output_file = os.path.abspath(os.path.join(output_path, f"{filename_prefix}.{extension}"))
            try:
                if extension in ["jpg", "jpeg"]:
                    img.save(output_file, quality=quality, optimize=True)
                elif extension == 'webp':
                    img.save(output_file, quality=quality, lossless=lossless_webp, exif=exif_data)
                elif extension == 'png':
                    img.save(output_file, pnginfo=exif_data, optimize=True)
                else:
                    img.save(output_file)
            except Exception as e:
                print(e)

    def save_text(self, text, output_file_path, file_name, file_extension, overwrite, number_padding,
                  image=None, prompt=None, extra_pnginfo=None):

        if isinstance(file_name, list):
            file_name = file_name[0]

        if output_file_path == "" or file_name == "":
            log_node_warn("Save Text", "No file details found. No file output.")
            return ()

        if not os.path.exists(output_file_path):
            os.makedirs(output_file_path)

        index = 1
        while True:
            suffix = f"_{str(index).zfill(number_padding)}"
            numbered_file = f"{file_name}{suffix}.{file_extension}"
            filepath = os.path.join(output_file_path, numbered_file)
            if not os.path.exists(filepath):
                break
            index += 1

        filepath_print = filepath.replace("\\", "/")
        log_node_info("Save Text", f"Saving to {filepath_print}")

        if file_extension == "csv":
            text_list = [line.strip() for line in text.split("\n")]
            with open(filepath, "w", newline="", encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                for line in text_list:
                    csv_writer.writerow([line])
        else:
            with open(filepath, "w", newline="", encoding='utf-8') as text_file:
                text_file.write(text)

        result = {"result": (text, None)}

        if image is not None:
            image_prefix = os.path.splitext(numbered_file)[0]
            imagepath = os.path.join(output_file_path, image_prefix)
            output_path = self.output_dir if output_file_path.strip() in ["", ".", "none"] else output_file_path

            if not os.path.isabs(output_path):
                output_path = os.path.join(folder_paths.output_directory, output_path)

            if not os.path.exists(output_path):
                os.makedirs(output_path, exist_ok=True)

            images = torch.cat([image], dim=0)
            self.save_image(images, imagepath, 'png', 100, prompt, extra_pnginfo,
                            number_padding=number_padding, output_path=output_path)

            log_node_info("Save Text", f"Saving Image to {imagepath}")
            result['result'] = (text, image)

        return result
