from .mask_frame_cafe import maskframecafe   
from .RGBA2RGB import RGBA2RGB
from .get_pic_name import GPICNAME
from .load_img_from_path_1by1 import load_images_from_the_path_one_by_one
from .pixian_rmbg import PixianRMBG

WEB_DIRECTORY = "./js"

NODE_CLASS_MAPPINGS = {
    "自定义蒙版外框☕️": maskframecafe,
    "RGBA转为RGB☕️": RGBA2RGB,
    "获取图片名称☕️": GPICNAME,
    "从路径依次加载图片☕️": load_images_from_the_path_one_by_one,
    "Pixian RMBG☕️": PixianRMBG
    }