# ComfyUI-Cafe-Node
# 从路径依次加载图片☕️
批处理的数字即为执行次数

![image](https://github.com/user-attachments/assets/ca91dd64-29cf-46f7-b067-e5f40fb998b5)

例如：在“D:\Download\输入图片\JV图案分类汇总\植物花卉”文件夹中有如下图片：
```
植物花卉1.png
植物花卉10.png
植物花卉2.png
植物花卉3.png
植物花卉4.png
植物花卉5.png
植物花卉6.png
植物花卉7.png
植物花卉8.png
植物花卉9.png
```
那么设定批处理数量为10，即可遍历完所有图片；设定批处理数量为5，只会遍历到“植物花卉4.png”，下次再执行就会从“植物花卉5.png”开始

# 获取图片名称☕️
能获取图片路径中的图片名称（不包含后缀名）
搭配“从路径依次加载图片☕️”节点和[WAS插件](https://github.com/WASasquatch/was-node-suite-comfyui)的“Image Save”节点，可做到从保存图片文件名前缀即可区分由什么输入图生成，便于批量生成后的分析

![image](https://github.com/user-attachments/assets/cb40f6e4-c5de-4b42-9b4d-ebf7dd0def49)

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
