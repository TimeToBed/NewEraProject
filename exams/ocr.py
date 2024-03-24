import os
from paddleocr import PaddleOCR, draw_ocr
from pathlib import Path
import json
import imageio
from io import BytesIO
import cv2
import numpy as np

def get_contours(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    canny = cv2.Canny(blurred, 120, 255, 1)

    # Find contours in the image
    cnts = cv2.findContours(canny.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    # Obtain area for each contour
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in cnts]
    return contour_sizes

def select_cut(img, ocr):
    results = ''
    # 把选择题区域裁剪出来
    original_image=img
    H,W,_=original_image.shape
    image = original_image.copy()
    contour_sizes=get_contours(image)

    # Find maximum contour and crop for ROI section
    if len(contour_sizes) > 0:
        largest_contour = max(contour_sizes, key=lambda x: x[0])[1]
    
        x0, y0, w0, h0 = cv2.boundingRect(largest_contour)
        cv2.rectangle(image, (x0, y0), (x0 + w0, y0 + h0), (36, 255, 12), 2)
        ROI = original_image[y0:y0 + h0, x0:x0 + w0]
        
        # 将ROI附近的区域裁下来
        bbox=original_image[max(0,y0-h0//5): min(y0+h0+h0//5, H),  max(0,x0-w0//5):min(x0 + w0+w0//5, W)]
        contour_sizes=get_contours(bbox)
        
        row_col_list=[]
        for i in range(len(contour_sizes)):

            contour_size = contour_sizes[i][1]
            x, y, w, h = cv2.boundingRect(contour_size)
            row_col_list.append([round(w0/w), round(h0/h)])
        # print(row_col_list)
        
        res=0
        maxn=0
        for i in range(len(row_col_list)):
            t=row_col_list.count(row_col_list[i])
            #print(row_col_list[i], t, maxn)
            if t>maxn:
                res=i
                maxn=t
        col, row=row_col_list[res]
        # print(row, col)
        
        w=w0//col
        h=h0//row

        margin = 10
        for i in range(0,row,2):   #第i行，y坐标
            for j in range(col):      #第j列，x坐标
                x1,y1=int(x0+j*w), int(y0+i*h)
                # ROI = original_image[y1:y1 + h, x1:x1 + w]
                # 在ROI的定义中加上压缩的像素范围
                ROI = original_image[y1 + margin : y1 + h - margin, x1 + margin : x1 + w - margin]
                result = ocr.ocr(ROI, det=False, rec=True, cls=False)[0][0][0]
                results += (chr(ord(result) - 0xFEE0) if '０' <= result <= '９' else result) + '\n'
                # print(y1,y1 + h, x1,x1 + w)
                
                x1,y1=int(x0+j*w), int(y0+i*h+h)
                # ROI = original_image[y1:y1 + h, x1:x1 + w]
                ROI = original_image[y1 + margin : y1 + h - margin, x1 + margin : x1 + w - margin]
                result = ocr.ocr(ROI, det=False, rec=True, cls=False)[0][0][0]
                results += (chr(ord(result) - 0xFEE0) if 'Ａ' <= result <= 'Ｚ' else result) + '\n'
                
    # 将原图选出来的区域用白色mask掉
    mask = np.ones_like(original_image)
    cv2.rectangle(mask, (x0, y0), (x0 + w0, y0 + h0), (255, 255, 255), -1)
    original_image = cv2.bitwise_or(original_image, mask)
    
    return original_image, results

def ocr_progress(img, ocr):
    height, width, _ = img.shape
    
    
    # 第一次纯检测
    result = ocr.ocr(img, det=True, rec=False, cls=False)
    
    # 去除重复检测框
    threshold = 50
    for idx in range(len(result)):
        res = result[idx]
        # 先对框从上到下排序
        y_values = [np.min([box[i][1] for i in range(4)]) for box in res]
        # 获取 y 值的排序的索引
        sorted_indices = np.argsort(y_values)
        # 根据索引排序框
        res = [[[int(coordinate) for coordinate in point] for point in box] for box in [res[i] for i in sorted_indices]]
        # 获取每个框的 y_min 和 y_max
        y_mins = [np.min([box[i][1] for i in range(4)]) for box in res]  # 找到每个框的最小 y 值，相当于框的上边界
        y_maxs = [np.max([box[i][1] for i in range(4)]) for box in res]  # 找到每个框的最大 y 值，相当于框的下边界

        # # 计算每个框的高度 (y_max - y_min)
        # heights = [ymax - ymin for ymax, ymin in zip(y_maxs, y_mins)]

        #  我们先假设每个框都需要保留
        keep = [True] * len(res)

        # 遍历每一个检测框
        for i in range(len(res)):
            if keep[i]:
                # 对于每个还未被过滤掉的框
                for j in range(i + 1, len(res)):
                    # 判断两个框是否在同一行的阈值设置为平均框高重合率在80%
                    # threshold = 0.6 *(heights[i] + heights[j])
                    # 如果框 j 和框 i 在同一行
                    if abs(y_mins[i] - y_mins[j]) < threshold and abs(y_maxs[i] - y_maxs[j]) < threshold:  # 你需要根据实际情况设定适合的 threshold
                        # 如果框 j 的高度小于框 i，则删除框 j
                        # 取y_min最小的框的上侧，y_max最大的框的下侧
                        new_box_ymin = np.min([res[i], res[j]], axis=0)
                        new_box_ymax = np.max([res[i], res[j]], axis=0)
                        res[i] = [new_box_ymin[0], new_box_ymin[1], new_box_ymax[2], new_box_ymax[3]]
                        keep[j] = False

        # 最后，我们只保留那些我们确定需要保留的框
        filtered_boxes = [box for keep, box in zip(keep, res) if keep]
                        
    # 第二次纯识别
    # img_copy2 = np.copy(img)
    results = ''
    # start_time_rec = time.time()
    for line in filtered_boxes:
        coords = np.array(line, dtype=np.float32)
        # 获取检测框的y轴最小和最大值
        y_min = int(np.round(np.min(coords[:, 1])))
        y_max = int(np.round(np.max(coords[:, 1])))
        
        # 切割整行
        crop_img = img[y_min:y_max, 0:width].copy()
        
        # 对切割部分进行识别
        crop_result = ocr.ocr(crop_img, det=False, rec=True, cls=False)
        
        # 在原始图上标出这一行
        # cv2.rectangle(img_copy2, (0, y_min), (width, y_max), color=(0, 255, 0), thickness=2)
        
        # 打印识别结果
        print(crop_result[0][0][0])
            
        results += crop_result[0][0][0] + '\n'

    return results

def ocr_jsonsave(result, img_path, json_dir):
    """
        result: paddleocr识别结果
        img_path: 图片路径
        json_dir: json文件保存的文件夹路径
    """
    # 得到图片名称
    imgname_with_ext = os.path.basename(img_path)
    imgname, ext = os.path.splitext(imgname_with_ext)
    print(imgname)
    # 判断json文件夹是否存在
    if os.path.exists(json_dir):
        print("Folder exists.")
    else:
        print("Folder does not exist.")
        os.mkdir(json_dir)
    # 将结果存入json文件中
    json_path = os.path.join(json_dir, imgname + ".json")
    with open(json_path, 'w', encoding='utf-8') as f:
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                coords, contents, confidence = line[0], line[1][0], line[1][1]
                data = {
                    'coords': coords,
                    'contents': contents,
                    'confidence': confidence
                }
                json.dump(data, f, ensure_ascii=False)
                f.write('\n')
    return json_path
    
def get_weights_path():

    # 获取当前文件所在的目录的上一层目录
    parent_dir_path = Path(os.path.relpath(__file__)).parent.parent
    return os.path.join(parent_dir_path,'model_weights')

def ocr_getresult(sftp, image_path):
    """
        img_path: 图片路径，从数据库读取
        返回：识别结果
    """
    remote_file = sftp.open(image_path, 'rb')

    # 转换图片到numpy数组
    np_image = imageio.imread(BytesIO(remote_file.read()))
    
    weights_path = get_weights_path()
    # 图片OCR识别
    ocr = PaddleOCR(use_angle_cls=True, lang="ch",use_gpu=True,
 
                rec_model_dir= os.path.join(weights_path,'ch_PP-OCRv4_rec_infer'),
 
                cls_model_dir= os.path.join(weights_path,'ch_ppocr_mobile_v2.0_cls_infer'),
 
                det_model_dir= os.path.join(weights_path,'ch_PP-OCRv4_det_infer')) # need to run only once to download and load model into memory
    
    result = ocr.ocr(np_image, cls=True)  
      
    return result
    