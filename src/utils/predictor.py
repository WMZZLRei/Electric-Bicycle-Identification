import os
import sys

import cv2
import numpy as np
import onnxruntime as rt
import torch


class ObjectDetector:
    def __init__(self, **kwargs):
        current_dir = getattr(sys, '_MEIPASS', os.getcwd())
        """
        初始化方法

        Parameters:
            image_data (image_data): 图片数据
            confidence_threshold (float): 置信度阈值
            iou_threshold (float, optional): IOU阈值
            model_path (str): 模型文件路径
            draw_text (bool, optional): 是否绘制物体标签，默认为True
            save (bool, optional): 是否保存，默认为False
            save_path (str, optional): 保存路径，默认为None
            save_name (str, optional): 保存的文件名，默认为result.jpg
            use_gpu (bool, optional): 是否使用GPU，默认为True
        """
        # 实例时初始化参数
        self.image_data = kwargs.get("image_data")
        self.confidence_threshold = kwargs.get("confidence_threshold", 0.5)
        self.iou_threshold = kwargs.get("iou_threshold", 0.4)
        self.model_path = kwargs.get("model_path", current_dir+"./model/YOLOv8-CBAM-fuse.onnx")
        self.draw_text = kwargs.get("draw_text", False)
        self.save = kwargs.get("save", False)
        self.save_path = kwargs.get("save_path", "../resources/save")
        self.save_name = kwargs.get("save_name", "/result.jpg")
        self.use_gpu = kwargs.get("use_gpu", True)

        self.sess = None

        # 类别字典
        self.dic = {
            0: "ElectricBicycle"
        }
        self.class_list = list(self.dic.values())
        self.std_h = 640
        self.std_w = 640

        self.initialize_session()

    def resize_image(self):
        """
            对输入图像进行resize

        Returns:指定尺寸的图像
        """
        image = self.image_data
        ih, iw, _ = self.image_data.shape
        h, w = self.std_h, self.std_w
        # 进行letterbox变换
        scale = min(w / iw, h / ih)
        nw = int(iw * scale)
        nh = int(ih * scale)
        image = cv2.resize(image, (nw, nh), interpolation=cv2.INTER_LINEAR)
        # 生成画布
        image_resize = np.ones((h, w, 3), dtype=np.uint8) * 128
        # 将image放在画布中心区域-letterbox
        image_resize[(h - nh) // 2: (h - nh) // 2 + nh, (w - nw) // 2:(w - nw) // 2 + nw, :] = image
        return image_resize

    def img2input(self, img):
        """
            将图像转换为模型输入格式。
        return：转换后的模型输入数据
        """
        img = np.transpose(img, (2, 0, 1))
        img = img / 255
        return np.expand_dims(img, axis=0).astype(np.float32)

    def std_output(self, pred):
        """
        将（1，84，8400）处理成（8400， 85）  85= box:4  conf:1 cls:80
        """
        pred = np.squeeze(pred)
        pred = np.transpose(pred, (1, 0))
        pred_class = pred[..., 4:]
        pred_conf = np.max(pred_class, axis=-1)
        pred = np.insert(pred, 4, pred_conf, axis=-1)
        return pred

    def xywh2xyxy(self, *box):
        """
        将xywh转换为左上角点和左下角点,用于get_inter函数计算相交部分
        Args:
            box:
        Returns: x1y1x2y2
        """
        ret = [box[0] - box[2] // 2, box[1] - box[3] // 2,
               box[0] + box[2] // 2, box[1] + box[3] // 2]
        return ret

    def get_inter(self, box1, box2):
        """
        计算相交部分面积,用于get_iou函数计算交并比
        Args:
            box1: 第一个框
            box2: 第二个狂
        Returns: 相交部分的面积
        """
        x1, y1, x2, y2 = self.xywh2xyxy(*box1)  # 把YOLO的box转换成左上角点和右下角点
        x3, y3, x4, y4 = self.xywh2xyxy(*box2)  # 把YOLO的box转换成左上角点和右下角点
        # 验证是否存在交集
        if x1 >= x4 or x2 <= x3:
            return 0
        if y1 >= y4 or y2 <= y3:
            return 0
        # 将x1,x2,x3,x4排序，因为已经验证了两个框相交，所以x3-x2就是交集的宽
        x_list = sorted([x1, x2, x3, x4])
        x_inter = x_list[2] - x_list[1]
        # 将y1,y2,y3,y4排序，因为已经验证了两个框相交，所以y3-y2就是交集的宽
        y_list = sorted([y1, y2, y3, y4])
        y_inter = y_list[2] - y_list[1]
        # 计算交集的面积
        inter = x_inter * y_inter
        return inter

    def get_iou(self, box1, box2):
        """
        计算交并比： (A n B)/(A + B - A n B)
        Args:
            box1: 第一个框
            box2: 第二个框
        Returns:  # 返回交并比的值
        """
        box1_area = box1[2] * box1[3]  # 计算第一个框的面积
        box2_area = box2[2] * box2[3]  # 计算第二个框的面积
        inter_area = self.get_inter(box1, box2)  # 计算交集的面积
        union = box1_area + box2_area - inter_area  # (A n B)/(A + B - A n B)
        iou = inter_area / union
        return iou

    def nms(self, pred, conf_thres, iou_thres):
        """
        非极大值抑制nms
        Args:
            pred: 模型输出特征图
            conf_thres: 置信度阈值
            iou_thres: iou阈值
        Returns: 输出后的结果
        """
        box = pred[pred[..., 4] > conf_thres]  # 置信度筛选
        cls_conf = box[..., 5:]
        cls = []
        for i in range(len(cls_conf)):
            cls.append(int(np.argmax(cls_conf[i])))
        total_cls = list(set(cls))  # 记录图像内共出现几种物体
        output_box = []
        # 每个预测类别分开考虑
        for i in range(len(total_cls)):
            clss = total_cls[i]
            cls_box = []
            temp = box[:, :6]
            for j in range(len(cls)):
                # 记录[x,y,w,h,conf(最大类别概率),class]值
                if cls[j] == clss:
                    temp[j][5] = clss
                    cls_box.append(temp[j][:6])
            #  cls_box 里面是[x,y,w,h,conf(最大类别概率),class]
            cls_box = np.array(cls_box)
            sort_cls_box = sorted(cls_box, key=lambda x: -x[4])  # 将cls_box按置信度从大到小排序
            max_conf_box = sort_cls_box[0]
            output_box.append(max_conf_box)
            sort_cls_box = np.delete(sort_cls_box, 0, 0)
            # 对除max_conf_box外其他的框进行非极大值抑制
            while len(sort_cls_box) > 0:
                # 得到当前最大的框
                max_conf_box = output_box[-1]
                del_index = []
                for j in range(len(sort_cls_box)):
                    current_box = sort_cls_box[j]
                    iou = self.get_iou(max_conf_box, current_box)
                    if iou > iou_thres:
                        # 筛选出与当前最大框Iou大于阈值的框的索引
                        del_index.append(j)
                # 删除这些索引
                sort_cls_box = np.delete(sort_cls_box, del_index, 0)
                if len(sort_cls_box) > 0:
                    # 我认为这里需要将clas_box先按置信度排序， 才能每次取第一个
                    output_box.append(sort_cls_box[0])
                    sort_cls_box = np.delete(sort_cls_box, 0, 0)
        return output_box

    def cod_trf(self, result, pre, after):
        """
        因为预测框是在经过letterbox后的图像上做预测所以需要将预测框的坐标映射回原图像上
        Args:
            result:  [x,y,w,h,conf(最大类别概率),class]
            pre:    原尺寸图像
            after:  经过letterbox处理后的图像
        Returns: 坐标变换后的结果,
        """
        # 检查result是否为空列表,为空表示没有检测到物体
        if len(result) == 0:
            return result  # 如果结果为空，直接返回空列表
        # 如果result不为空，执行后续处理逻辑
        res = np.array(result)
        x, y, w, h, conf, cls = res.transpose((1, 0))
        x1, y1, x2, y2 = self.xywh2xyxy(x, y, w, h)  # 左上角点和右下角的点
        h_pre, w_pre, _ = pre.shape
        h_after, w_after, _ = after.shape
        scale = max(w_pre / w_after, h_pre / h_after)  # 缩放比例
        h_pre, w_pre = h_pre / scale, w_pre / scale  # 计算原图在等比例缩放后的尺寸
        x_move, y_move = abs(w_pre - w_after) // 2, abs(h_pre - h_after) // 2  # 计算平移的量
        ret_x1, ret_x2 = (x1 - x_move) * scale, (x2 - x_move) * scale
        ret_y1, ret_y2 = (y1 - y_move) * scale, (y2 - y_move) * scale
        ret = np.array([ret_x1, ret_y1, ret_x2, ret_y2, conf, cls]).transpose((1, 0))
        return ret

    def draw(self, res, image, cls):
        """
        将预测框绘制在image上

        Args:
            res: 预测框数据，格式为列表，每个元素为一个预测框的信息，包括左上角坐标、右下角坐标、置信度、类别id和类别概率。
            image: 原图，将在此图上绘制预测框。
            cls: 类别列表，用于标注预测框的类别，每个元素为类别名称。

        Returns:
            绘制了预测框的图像。
        """
        draw_text = self.draw_text
        for r in res:
            # 根据预测框的坐标，在图像上画出矩形框
            image = cv2.rectangle(image, (int(r[0]), int(r[1])), (int(r[2]), int(r[3])), (0, 0, 255), 2)
            # 根据预测框的类别信息，生成类别标签，并计算合适的字体大小
            if draw_text:
                # 表明类别
                text = "{}:{}".format(cls[int(r[5])], round(float(r[4]), 2))
                h, w = int(r[3]) - int(r[1]), int(r[2]) - int(r[0])  # 计算预测框的长宽
                font_size = min(h / 640, w / 640) * 2  # 计算字体大小（随框大小调整）
                image = cv2.putText(image, text, (max(10, int(r[0])), max(20, int(r[1]))), cv2.FONT_HERSHEY_COMPLEX,
                                    max(font_size, 0.3), (0, 0, 255), 1)  # max()为了确保字体不过界
        return image

    def initialize_session(self):
        """
        初始化模型会话，根据是否使用GPU来配置会话选项。
        """
        # 配置会话选项
        sess_options = rt.SessionOptions()

        if self.use_gpu:
            if check_gpu_available():
                print("检测到 GPU 可用. 优先使用 GPU 计算.")
                providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']  # 如果 GPU 可用，更新为 GPU 和 CPU 提供商
            else:
                print("未检测到 GPU. 使用 CPU 计算.")
                providers = ['CPUExecutionProvider']  # 默认设置为 CPU
        else:
            providers = ['CPUExecutionProvider']  # 默认设置为 CPU

        sess_options.graph_optimization_level = rt.GraphOptimizationLevel.ORT_ENABLE_ALL  # 最高级别的图形优化
        sess_options.intra_op_num_threads = 1  # 设置为单线程以避免线程间竞争
        sess_options.execution_mode = rt.ExecutionMode.ORT_SEQUENTIAL  # 使用顺序执行模式
        # 创建模型推理会话
        self.sess = rt.InferenceSession(self.model_path, sess_options=sess_options, providers=providers)

    def run_image(self, image_data):
        """
        执行模型推理，并将结果返回。
        """
        self.image_data = image_data
        image_resize = self.resize_image()  # 调整图片尺寸
        image_model_data = self.img2input(image_resize)  # 将图片转换为模型输入格式

        input_name = self.sess.get_inputs()[0].name  # 传递张量
        label_name = self.sess.get_outputs()[0].name
        pred = self.sess.run([label_name], {input_name: image_model_data})[0]  # (bs, 84=80cls+4reg, 8400=3种尺度的特征图叠加)
        pred = self.std_output(pred)  # 将预测结果标准化
        result = self.nms(pred, 0.5, 0.4)  # [x,y,w,h,conf(最大类别概率),class]
        result = self.cod_trf(result, self.image_data, image_resize)  # 坐标转换
        output_image = self.draw(result, self.image_data, self.class_list)
        if self.save:
            print("保存图片到:", self.save_path + self.save_name)
            cv2.imwrite(self.save_path + self.save_name, output_image)
        return output_image

    def run_video(self, frame):
        """
        执行模型推理，并将结果返回。
        """
        self.image_data = frame
        image_resize = self.resize_image()  # 调整图片尺寸
        image_model_data = self.img2input(image_resize)  # 将图片转换为模型输入格式

        input_name = self.sess.get_inputs()[0].name  # 传递张量
        label_name = self.sess.get_outputs()[0].name
        pred = self.sess.run([label_name], {input_name: image_model_data})[0]  # (bs, 84=80cls+4reg, 8400=3种尺度的特征图叠加)
        pred = self.std_output(pred)  # 将预测结果标准化
        result = self.nms(pred, 0.5, 0.4)  # [x,y,w,h,conf(最大类别概率),class]
        result = self.cod_trf(result, self.image_data, image_resize)  # 坐标转换
        output_image = self.draw(result, self.image_data, self.class_list)
        return output_image

    def run_camera(self, image_data):
        """
            执行模型推理，并将结果返回。
        Args:
            image_data: 图像数据
        Returns:
            output_image: 处理后的图像
            result: 检测结果
        """
        self.image_data = image_data
        image_resize = self.resize_image()  # 调整图片尺寸
        image_model_data = self.img2input(image_resize)  # 将图片转换为模型输入格式

        input_name = self.sess.get_inputs()[0].name  # 传递张量
        label_name = self.sess.get_outputs()[0].name
        pred = self.sess.run([label_name], {input_name: image_model_data})[
            0]  # (batch size, 5=1cls+4reg, 8400=3种尺度的特征图叠加)
        pred = self.std_output(pred)  # 将预测结果标准化 对应4个预测框+1个置信度（最大类别概率）+1类别概率 (8400, 5)
        result = self.nms(pred, self.confidence_threshold, self.iou_threshold)  # [x,y,w,h,conf(最大类别概率),class]

        result = self.cod_trf(result, self.image_data, image_resize)  # 后处理
        output_image = self.draw(result, self.image_data, self.class_list)
        return output_image, result


def check_gpu_available():
    try:
        if torch.cuda.is_available():
            return True
    except ImportError:
        pass

    try:
        import tensorflow as tf
        if tf.test.is_gpu_available():
            return True
    except ImportError:
        pass

    return False
