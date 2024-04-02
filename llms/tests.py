from django.test import TestCase
import json
import os,sys
sys.path.append(os.getcwd())
from demo import settings
from django.http import JsonResponse
from LLM_package import *

# Create your tests here.4

def LLM_preprocess(exam_id):
    print('LLM预处理 从前端传回来的考试exam_id：',exam_id)
    load_ocr(r'D:\Competition\NewEraProject\server\.cache\3.json')
    exam_analysis_path = os.path.join(settings.MEDIA_URL,"2020年全国卷Ⅰ语文高考试题完整版.json")
    with open(exam_analysis_path, 'r', encoding='utf-8') as exam_json:
        exam_detail_info = json.load(exam_json)
    return JsonResponse(exam_detail_info, safe=False)

LLM_preprocess(1)
