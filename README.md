# ElectricBicycleDetection

## 简介
ElectricBicycleDetection（电动自行车识别系统）是一个用于检测电动自行车的项目，为本人毕业设计作品。该项目该项目的GUI采用PYQT5构建，后端推理部分使用ONNX，使用的模型是改进版的YOLOv8m，添加了CBAM模块。程序支持GPU加速，但需要有和ONNX-GPU对应的CUDA版本，否则将使用CPU进行推理。

## 目录
- [简介](#简介)
- [安装](#安装)
- [使用方法](#使用方法)
- [贡献](#贡献)
- [许可证](#许可证)
- [致谢](#致谢)
- [联系方式](#联系方式)

## 安装
1. 克隆仓库：
    ```bash
    git clone https://github.com/WMZZLRei/Electric-Bicycle-Identification.git
    ```
2. 进入项目目录：
    ```bash
    cd ElectricBicycleDetection
    ```
3. 安装依赖项：
    ```bash
    pip install -r requirements.txt
    ```

## 使用方法
该程序主要有三大功能：图片检测、视频检测、摄像头检测。

### 图片检测
1. 打开程序，选择“图片检测”功能。
2. 填入源文件路径、置信度、保存路径。
3. 点击“开始检测”按钮进行检测。

### 视频检测
1. 打开程序，选择“视频检测”功能。
2. 填入源文件路径、置信度、保存路径。
3. 点击“开始检测”按钮进行检测。

### 摄像头检测
1. 打开程序，选择“摄像头检测”功能。
2. 程序启动时会自动读取摄像头设备，可根据需要选择不同的摄像头。
3. 设定置信度。
4. 如果保存路径为空，依然可以进行检测，但不会保存视频。
5. 点击“开始检测”按钮进行检测。

## 贡献
欢迎任何形式的贡献！请先阅读[贡献指南](CONTRIBUTING.md)。

## 许可证
该项目使用MIT许可证，详情请参阅[LICENSE](LICENSE)文件。

## 致谢
感谢以下项目和工具的支持：
- [PYQT5](https://riverbankcomputing.com/software/pyqt/intro)
- [ONNX](https://onnx.ai/)
- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)

## 联系方式
如果有任何问题，请通过[GitHub Issues](https://github.com/WMZZLRei/Electric-Bicycle-Identification/issues)。
