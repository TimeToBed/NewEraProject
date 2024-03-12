from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import *  # assuming you have an Exam model
from exams.models import *
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, FileResponse
from django.core import serializers
import os
import json
from asgiref.sync import sync_to_async

from .LLM_package import *
from datetime import datetime
from demo import settings
import json
import shutil
# Create your views here.
import os
import json
import ast
import io
import base64
from asgiref.sync import sync_to_async

import paramiko
from datetime import datetime
from demo import settings
from django.db.models import Max
import posixpath
import stat
import json
import shutil
from paddleocr import PaddleOCR
from pathlib import Path
import imageio
from io import BytesIO
import tempfile


def LLM_preprocess(request, exam_id):
    print('LLM预处理 从前端传回来的考试exam_id：',exam_id)
    exam_analysis_path = os.path.join(settings.MEDIA_URL,"2020年全国卷Ⅰ语文高考试题完整版.json")
    with open(exam_analysis_path, 'r', encoding='utf-8') as exam_json:
        exam_detail_info = json.load(exam_json)
    return JsonResponse(exam_detail_info, safe=False)


def LLM_preview(request, exam_id):
    from docx2pdf import convert
    import fitz

    print('LLM预览 从前端传回来的考试exam_id：',exam_id)
    exam = Exams.objects.filter(id=exam_id)[0]
    print(exam)
    paper_path = exam.paper_identity_path
    print(paper_path)
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
    sftp = ssh.open_sftp()
    paper_data = sftp.file(paper_path, 'rb').read()
    tmppath='../server/tmp.docx'
    pdfpath=tmppath.replace('docx','pdf')
    with open(tmppath, 'wb') as local_file:
        local_file.write(paper_data)
    print('convert to pdf')
    #convert(tmppath, pdfpath)
    doc=fitz.open(pdfpath)
    images=[]
    for pg in range(doc.page_count):
        page = doc[pg]
        pix = page.get_pixmap(alpha=False)          # 默认是720*x尺寸

        images.append(pix)
        pix.save('../server/'+'images_%s.jpg' % pg)

    images_base64 = [base64.b64encode(img.tobytes(output='jpg')).decode('utf-8') for img in images]

    
    sftp.close()
    ssh.close()

    os.remove(tmppath)
    return JsonResponse(images_base64, safe=False)



async def test_p(p_test_problem):
    #可以直接将这两行代码放入指定位置，进行流式异步传输
    async for content in analysis_problem(p_test_problem):
        print(content, end="")

async def calculate_context(result):
    context = ""
    async for content in analysis_problem(result):
        context += content
    return context

#@csrf_exempt
async def rectangle(request):
    print('rectangle')
    json_dir = './server/ocr'
    if request.method == 'POST':
        x1 = int(request.POST.get('x1'))
        x2 = int(request.POST.get('x2'))
        y1 = int(request.POST.get('y1'))
        y2 = int(request.POST.get('y2'))
        name=request.POST.get('name')
        print('rectangle:POST')

        name=name.replace(name.split('.')[-1],'json')
        json_path=os.path.join(json_dir, name)
        
        file = open(json_path, 'r', encoding='utf-8')
        data = []
        for line in file.readlines():
           dic = json.loads(line)
           data.append(dic)
        result=''
        for item in data:
            #item['coords']=ast.literal_eval(item['coords'])
            coords1=item['coords'][0]
            coords2=item['coords'][2]
            if x1<=coords1[0] and y1<=coords1[1] and x2>=coords2[0] and y2>=coords2[1]:
                result+=item['contents']
        print('result:', result)
        context=''
        async for content in analysis_problem(result):
            context+=content
            print(content, end="")
            

        # return JsonResponse({'status': 'ok', 'message': 'Data received.'})
        return JsonResponse({'status': 'ok', 'message': 'Data received.', 'result':context}) 
    return JsonResponse({'status': 'false', 'message': 'Error.'})
    #return await HttpResponse("Hello world ! ")