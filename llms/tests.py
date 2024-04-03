from django.test import TestCase
import json
import os,sys,shutil
import json, base64, paramiko, os
sys.path.append(os.getcwd())
from demo import settings
from django.http import JsonResponse
from LLM_package import *

# Create your tests here.4

def del_object(*args):
    for obj in args:
        try:
            obj.close()
        except AttributeError:
            print(f'The object {obj} does not have a close method.')
        except Exception as e:
            print(f'An error occurred when closing object {obj}: {e}')

def clean_server_cache():

    for file_name in os.listdir(settings.TEMP_URL):
        file_path = os.path.join(settings.TEMP_URL, file_name)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)  # 移除文件或符号链接
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)  # 递归删除一个目录

def ssh_connect():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=settings.Remote_HOST, username=settings.Remote_user, password=settings.Remote_password, port=settings.Remote_PORT)
        print("连接成功")
    except paramiko.AuthenticationException:
        print("认证失败")
        return 'SSH Authentication failed'
    except paramiko.SSHException as e:
        print("连接错误：", str(e))
        return 'SSH connection error'
    return ssh

def LLM_preprocess(exam_id):
    print('LLM预处理 从前端传回来的考试exam_id：',exam_id)

    ocr_path = r'D:\Competition\NewEraProject\server\.cache\3.json'
    doc_path = r'D:\Competition\NewEraProject\server\.cache\2020年全国卷Ⅰ语文高考试题.docx'
    json_path = r'D:\Competition\NewEraProject\server\.cache\exam_detail.json'
    init_llm_json(doc_path,ocr_path,json_path)
    exam_analysis_path = os.path.join(settings.MEDIA_URL,"2020年全国卷Ⅰ语文高考试题完整版.json")
    with open(exam_analysis_path, 'r', encoding='utf-8') as exam_json:
        exam_detail_info = json.load(exam_json)
    return JsonResponse(exam_detail_info, safe=False)


