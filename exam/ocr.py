import os
from paddleocr import PaddleOCR, draw_ocr
from pathlib import Path
import json

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

def ocr_getresult(image_path, ocr_path):
    """
        img_path: 图片路径，从数据库读取
        ocr_path: 结果保存的文件夹路径
        返回：json文件的路径
    """
    img_path = os.path.abspath(image_path)
    json_dir = os.path.abspath(ocr_path)
    # 判断图片路径是否存在
    if os.path.isfile(img_path):
        print(img_path, "OK")
    else:
        print(img_path, "not exist")
    
    weights_path = get_weights_path()
    # 图片OCR识别
    ocr = PaddleOCR(use_angle_cls=True, lang="ch",use_gpu=True,
 
                rec_model_dir= os.path.join(weights_path,'ch_PP-OCRv4_rec_infer'),
 
                cls_model_dir= os.path.join(weights_path,'ch_ppocr_mobile_v2.0_cls_infer'),
 
                det_model_dir= os.path.join(weights_path,'ch_PP-OCRv4_det_infer')) # need to run only once to download and load model into memory
    
    result = ocr.ocr(img_path, cls=True)  
    
    # 将结果保存到json文件中
    json_path = ocr_jsonsave(result, img_path, json_dir)    
    return result, json_path
    