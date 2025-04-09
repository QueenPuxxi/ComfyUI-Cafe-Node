import os

class GPICNAME:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):

        return {
            "required": {
                "image_path": ("STRING",),
            },
        }

    RETURN_TYPES = ("STRING",)
    #RETURN_NAMES = ("image_output_name",)

    FUNCTION = "get_picname"

    #OUTPUT_NODE = False

    CATEGORY = "图像处理☕️"

    def get_picname(self, image_path):
        # Extract the file name using os.path for better cross-platform support
        image_path = image_path.replace("\\", "/")
        image_path = os.path.normpath(image_path)
        image_name_with_ext = os.path.basename(image_path)
        # Split the file name and extension
        image_name, _ = os.path.splitext(image_name_with_ext)
        print(image_name)
        
        return (image_name,)
