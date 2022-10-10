## 安装

安装anaconda(conda虚拟环境)

在目录终端进行操作：

```
conda create -n yolotracking python=3.6
conda activate yolotracking
pip install --upgrade pip # 升级pip库管理工具

pip install -r requirements.txt -i https://pypi.doubanio.com/simple #安装环境库
#如果torch安装失败
#pip install torch --no-cache-dir

```
下载预训练模型[yolov7](https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7.pt)到文件根目录

## 运行

```
python detect_and_track.py --source 0	#相机设备
									RGB.mp4 #本地视频文件
```

