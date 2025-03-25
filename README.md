# ComfyUI-Cafe-Node
# RGBA转为RGB☕️
## ！！！强烈建议搭配[ComfyUI-Light-Tool](https://github.com/ihmily/ComfyUI-Light-Tool)的加载图像节点一起使用，官方的加载图像节点不适用！！！

## 效果预览
![image](https://github.com/user-attachments/assets/fc68daf8-fb4a-49d2-87b2-1958f747d6e0)

# 自定义蒙版外框☕️
节点参数：
- expand: 扩展像素数
- incremental_expandrate: 扩展像素增量
- tapered_corners: 边缘是否倒角
- flip_input: 是否反转输入的蒙版
- blur_radius: 扩展的高斯模糊半径
- lerp_alpha: 蒙版插值因子
- decay_factor: 蒙版衰减因子
- fill_holes: 是否填充内部空洞

![image](https://github.com/user-attachments/assets/b184f317-7a2f-4703-b6f0-014bc83980c9)

## 效果预览
![image](https://github.com/user-attachments/assets/5dc339b1-6320-478c-9eed-046edc3fad8b)

## 示例工作流
![示例](https://github.com/user-attachments/assets/4022a595-407d-4b4d-8b0a-10065a822018)

# 安装
请确保您已经安装了[ComfyUI](https://github.com/comfyanonymous/ComfyUI)
```
cd custom_nodes
git clone https://github.com/QueenPuxxi/ComfyUI-Cafe-Node.git
cd ComfyUI-Cafe-Node
pip install -r requirements.txt
```
安装完成后，需要重启ComfyUI才能使用该节点
