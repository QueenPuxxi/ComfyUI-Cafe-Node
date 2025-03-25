import cv2
import numpy as np
import torch
import comfy

class RGBA2RGB:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "rgba2rgb"
    CATEGORY = "图像处理☕️"
    DESCRIPTION = """将RGBA图像的透明部分转为非透明部分的平均像素相反值，以此突出主体"""

    def rgba2rgb(self, image):
        # 确保输入是 NumPy 数组并且具有正确的形状
        image_0 = image
        if len(image.shape) == 4:
            image = image.squeeze(0)  # 移除批次维度如果存在
        
        # 检查图像是否具有 alpha 通道（RGBA）
        if image.shape[-1] == 4:
            # 将图像转换为 NumPy 数组如果它还不是
            if isinstance(image, torch.Tensor):
                image = image.cpu().numpy()
            
            print(f"输入图像形状: {image.shape}, 数据类型: {image.dtype}")
            
            # 处理图像以从 RGBA 转换为 RGB
            rgb_image = self.process_rgba2rgb(image)
            
            # 将结果转换回 PyTorch 张量
            rgb_image_tensor = torch.from_numpy(rgb_image).unsqueeze(0).float()
        
        else:
            # 如果没有 alpha 通道，直接返回原始图像
            rgb_image_tensor = image_0
        
        return (rgb_image_tensor,)

    def process_rgba2rgb(self, im):
        if im is not None and im.shape[-1] == 4:
            # 提取透明度通道
            alpha_channel = im[:, :, 3]
            mask = alpha_channel != 0  # 非透明区域的掩码
            
            print(f"Alpha 通道形状: {alpha_channel.shape}")
            print(f"非透明像素数量: {np.sum(mask)}")
            
            # 提取非透明像素的 RGB 值
            non_transparent_pixels = im[mask][:, :3]
            
            if non_transparent_pixels.size > 0:
                print(f"非透明像素形状: {non_transparent_pixels.shape}")
                print(f"前5个非透明像素示例: {non_transparent_pixels[:5]}")  # 打印前5个非透明像素
                
                # 计算非透明像素的 RGB 均值
                mean_color_float = np.mean(non_transparent_pixels, axis=0)
                mean_color_uint8 = (mean_color_float * 255).astype(np.uint8)
                opposite_color_uint8 = 255 - mean_color_uint8  # 计算相反色
                print(f"计算得到的均值颜色 (float): {mean_color_float}")
                print(f"计算得到的均值颜色 (uint8): {mean_color_uint8}")
                print(f"计算得到的相反颜色 (uint8): {opposite_color_uint8}")

                # 替换透明像素的 RGB 值为计算得到的相反色
                opposite_color_float = opposite_color_uint8 / 255.0  # 归一化到 [0, 1]
                im[~mask, :3] = opposite_color_float
                
            else:
                # 如果没有非透明像素，打印警告并将整张图像设为黑色
                print("警告：没有找到非透明像素，将整张图像设为黑色")
                mean_color_uint8 = [0, 0, 0]
                im[:, :, :3] = mean_color_uint8 / 255.0  # 保持浮点数范围 [0, 1]
            
            # 删除 alpha 通道
            im = im[:, :, :3]
        
        else:
            print("无效的图像输入或缺少 alpha 通道")
            im = np.zeros((im.shape[0], im.shape[1], 3), dtype=np.float32)
        
        return im
