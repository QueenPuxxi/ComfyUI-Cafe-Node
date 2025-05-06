import torch
import numpy as np
from PIL import Image
from io import BytesIO
import requests

class PixianRMBG:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "api_key": ("STRING", {"default": "", "multiline": False}),
                "api_secret": ("STRING", {"default": "", "multiline": False}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "pixian_rmbg"
    CATEGORY = "图像处理☕️"

    def pixian_rmbg(self, image, api_key, api_secret):
        print("📥 原始输入 image:")
        print("  type:", type(image))
        print("  shape:", image.shape)
        print("  dtype:", image.dtype)
        print("  max/min:", image.max().item(), image.min().item())

        image_0 = image  # 保底回退值

        if isinstance(image, torch.Tensor):
            image = image.detach().cpu().numpy()

        if image.ndim == 4:
            image = image.squeeze(0)  # (1, H, W, C) or (1, C, H, W)

        # 判断数据排列方式
        if image.shape[0] in [1, 3, 4]:  # (C, H, W)
            image = np.transpose(image, (1, 2, 0))  # → (H, W, C)

        image_uint8 = (image * 255).clip(0, 255).astype(np.uint8)
        pil_input = Image.fromarray(image_uint8)

        # 转 BytesIO 用于 POST 上传
        buf = BytesIO()
        pil_input.save(buf, format='PNG')
        buf.seek(0)

        # 调用 pixian_rmbg 抠图接口
        response = requests.post(
            'https://api.pixian_rmbg.ai/api/v2/remove-background',
            files={'image': buf},
            auth=(api_key, api_secret)
        )

        if response.status_code != 200:
            raise Exception(f"pixian_rmbg API 请求失败: {response.status_code} - {response.text}")

        # 返回的是 RGBA 图像
        result_img = Image.open(BytesIO(response.content)).convert("RGBA")
        result_np = np.array(result_img).astype(np.float32) / 255.0  # (H, W, 4)

        # 背景着色逻辑
        alpha = result_np[:, :, 3]
        mask = alpha != 0
        if np.sum(mask) > 0:
            fg = result_np[mask][:, :3]
            mean_color = np.mean(fg, axis=0)
            opposite_color = 1.0 - mean_color
            result_np[~mask, :3] = opposite_color
        else:
            result_np[:, :, :3] = 0.0  # 全透明时设为黑

        # 保留 alpha 通道并转为 tensor 格式 (1, H, W, 4)
        out_tensor = torch.from_numpy(result_np).unsqueeze(0).float()
        return (out_tensor,)
