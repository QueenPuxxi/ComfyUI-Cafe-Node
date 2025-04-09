import os
import json
import cv2
import glob
from PIL import Image, ImageOps, ImageSequence
import numpy as np
import torch
import node_helpers
import folder_paths as comfy_paths
import sys

sys.path.append(comfy_paths.base_path)

# ! GLOBALS
NODE_FILE = os.path.abspath(__file__)
WD_SUITE_ROOT = os.path.dirname(NODE_FILE)
WD_HISTORY_PATH = os.path.join(WD_SUITE_ROOT, 'wd_history.json')
TXT_DIR = os.path.join(WD_SUITE_ROOT, 'txt-dir')

class load_images_from_the_path_one_by_one:
    def __init__(self):
        self.history_json_path = WD_HISTORY_PATH
        self.data = None
        self.store_index = 0
        self.txt_name = None

        # Ensure txt-dir exists
        if not os.path.exists(TXT_DIR):
            os.makedirs(TXT_DIR)

        #json not exists code
        if not os.path.exists(self.history_json_path):
            pass

        # load history json
        if os.path.exists(self.history_json_path):
            try:
                with open(self.history_json_path, 'r', encoding='utf-8') as file:
                    self.data = json.load(file)
                print(f"成功加载 JSON 文件: {self.history_json_path}")
            except json.JSONDecodeError:
                print(f"错误: 文件 {self.history_json_path} 不是有效的 JSON 格式。")
            except Exception as e:
                print(f"加载 JSON 文件时出错: {e}")
        else:
            print(f"文件路径 {self.history_json_path} 不存在，正在创建一个新的空 JSON 文件...")
            try:
                self.data = {}  # 初始化为空字典
                with open(self.history_json_path, 'w', encoding='utf-8') as file:
                    json.dump(self.data, file, indent=4)
                print(f"成功创建空的 JSON 文件: {self.history_json_path}")
            except Exception as e:
                print(f"创建 JSON 文件时出错: {e}")
                self.data = None  # 在错误情况下，将 data 设为 None

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_dir_path": ("STRING", {"default": ''}),
                "mode": (["automatic", "index"],),
                "index": ("INT", {"default": 0, "min": 0, "step": 1}),
            },
        }

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("image", "image_path")
    FUNCTION = "start"

    CATEGORY = "输入Input☕️"

    def start(self, image_dir_path='', mode='automatic', index=0):
        image_dir_path = self.normalize_path(image_dir_path)
        self.store_index = index
        #PARTA 初始化和校验image list 相关信息
        # 1 判断文件夹路径是否存在问题
        image_paths, num_images, total_size = self.load_image_list(image_dir_path)
        # 2 校验history json 中 是否存在 同名文件夹 且 imagenum = len(image list)
            # 存在同名文件夹
                #判断数目和大小
                    #一致
                        #pass
                    #不一致
                        #删除原有txt和json的信息
                        #存当前文件夹的txt
                        #更新history json
            # 不存在同名文件夹
                #保存当前文件夹的txt
                #更新history json
        if image_dir_path not in self.data:
            print("channel 1")

            self.store_index = 0
            #保存txt
            self.txt_name = os.path.basename(os.path.normpath(image_dir_path)) + '-' + str(num_images) + "-" + str(
                total_size)
            txt_save_path = os.path.join(TXT_DIR, self.txt_name)

            with open(txt_save_path, 'w') as file:
                for line in image_paths:
                    file.write(line + '\n')

            print(f"数据已写入到 {txt_save_path} 文件中。")
            #更新json
            insert_data = {
                "txt_name": self.txt_name,
                "num_images": num_images,
                "total_size": total_size,
                "store_index": self.store_index
            }
            self.data[image_dir_path] = insert_data
        elif image_dir_path in self.data:
            print("**********************")
            print("channel 2")
            print(self.data)
            print("**********************")
            # 获取文件夹的值 并判断数量和大小是否一致
            image_data = self.data[image_dir_path]
            print("**********************")
            print("image data",image_data)
            print("**********************")
            if image_data['num_images'] == num_images and image_data['total_size'] == total_size:
                self.store_index = self.data[image_dir_path].get("store_index")
                pass
            else:
                self.store_index = 0
                #删除原本的txt
                txt_to_remove = os.path.join(TXT_DIR, self.data[image_dir_path]['txt_name'])
                if os.path.exists(txt_to_remove):
                    os.remove(txt_to_remove)
                del self.data[image_dir_path]
                #保存新的txt
                self.txt_name = os.path.basename(os.path.normpath(image_dir_path))+'-'+str(num_images)+"-"+str(total_size)
                txt_save_path = os.path.join(TXT_DIR,self.txt_name)
                with open(txt_save_path, 'w') as file:
                    for line in image_paths:
                        file.write(line + '\n')

                print(f"数据已写入到 {txt_save_path} 文件中。")
                #更新json
                insert_data = {
                    "txt_name": self.txt_name,
                    "num_images": num_images,
                    "total_size": total_size,
                    "store_index": self.store_index
                }
                self.data[image_dir_path] = insert_data
        else:
            print("*********")
            print("channel 3")
            print("*********")
            print(type(self.data))
            print(self.data)
            print("*********")
            print("*********")


        # PARTB 根据mode 读取对应的图片
        print("********* store_index 1 ***********",self.store_index)
        if mode == 'automatic':
            print("********** mode automatic **********")
            if self.store_index >= len(image_paths):
                self.store_index = 0
            image_path = image_paths[self.store_index]
            index_pic =  self.load_image(image_path)
            self.store_index += 1
            if self.store_index == len(image_paths):
                self.store_index = 0
            print("********* store_index 2 ***********", self.store_index)
        elif mode == 'index':
            self.store_index = index
            print("********** mode index *********")
            if self.store_index >= len(image_paths):
                self.store_index = self.store_index % len(image_paths)
            image_path = image_paths[self.store_index]
            index_pic =  self.load_image(image_path)
            print("******  *** store_index 2 ***********", self.store_index)

        print(f"*********type index_pic: {type(index_pic)} *********")


        #update store_index
        self.data[image_dir_path]["store_index"]  = self.store_index

        #update json file
        with open(WD_HISTORY_PATH, 'w') as file:
            json.dump(self.data, file, indent=4)
            print(f"数据已写入到 {WD_HISTORY_PATH} 文件中。")

        return (index_pic, image_path)


    def load_image_list(self, image_dir_path=''):
        image_paths = []
        total_size = 0

        if not os.path.exists(image_dir_path):
            raise FileNotFoundError(f"The directory path '{image_dir_path}' does not exist.")

        if not os.listdir(image_dir_path):
            raise ValueError(f"The directory '{image_dir_path}' is empty.")

        # 遍历文件夹和子目录下的图片文件
        for root, dirs, files in os.walk(image_dir_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    image_path = os.path.join(root, file)
                    image_paths.append(image_path)
                    total_size += os.path.getsize(image_path)

        num_images = len(image_paths)
        return image_paths, num_images, total_size

    def load_image(self, image_path):

        img = node_helpers.pillow(Image.open, image_path)

        output_images = []
        output_masks = []
        w, h = None, None

        excluded_formats = ['MPO']

        for i in ImageSequence.Iterator(img):
            i = node_helpers.pillow(ImageOps.exif_transpose, i)

            if i.mode == 'I':
                i = i.point(lambda i: i * (1 / 255))
            image = i.convert("RGB")

            if len(output_images) == 0:
                w = image.size[0]
                h = image.size[1]

            if image.size[0] != w or image.size[1] != h:
                continue

            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]
            if 'A' in i.getbands():
                mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                mask = 1. - torch.from_numpy(mask)
            else:
                mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")
            output_images.append(image)

        if len(output_images) > 1 and img.format not in excluded_formats:
            output_image = torch.cat(output_images, dim=0)
        else:
            output_image = output_images[0]

        return output_image

    def normalize_path(self, path):
        """标准化路径：处理多余斜杠并确保绝对路径"""
        # 使用os.path.abspath获取绝对路径
        abs_path = os.path.abspath(path)
        return abs_path
