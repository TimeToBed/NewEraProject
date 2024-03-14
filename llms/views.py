
from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, FileResponse, HttpResponse,HttpRequest
from demo import settings

from asgiref.sync import sync_to_async
import json, base64, paramiko, os
from pathlib import Path
from docx2pdf import convert
import fitz,io

from datetime import datetime
from .models import *  # assuming you have an Exam model
from exams.models import *
from .LLM_package import *
# Create your views here.

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

def ssh_execute_sudo_command(ssh, command):   
    stdin, stdout, stderr = ssh.exec_command(f"sudo -S {command}", get_pty=True)
    # 提供 sudo 密码
    stdin.write(settings.Remote_password + '\n')
    stdin.flush()
    output = stdout.read().decode('utf-8') 
    error = stderr.read().decode('utf-8')
    return output, error

def LLM_preprocess(request, exam_id):

    print('LLM_preprocess 从前端传回来的考试exam_id：',exam_id)
    exam_analysis_path = os.path.join(settings.MEDIA_URL,"2020年全国卷Ⅰ语文高考试题完整版.json")
    with open(exam_analysis_path, 'r', encoding='utf-8') as exam_json:
        exam_detail_info = json.load(exam_json)
    return JsonResponse(exam_detail_info, safe=False)

@csrf_exempt
def LLM_update(request:HttpRequest, exam_id):

    print('LLM_update 从前端传回来的考试exam_id：',exam_id)
    try:
        exam = Exams.objects.get(id=exam_id)
        exam_knowledge_path = exam.llm_knowledge_path

    except Exams.DoesNotExist:
        return JsonResponse({"result":"Error!"})
  
    if request.method == 'POST':
        ssh = ssh_connect()
        sftp = ssh.open_sftp()
        # 对 JSON 数据解码
        #data = json.loads(request.body.decode('utf-8')) #此时data为字典
        bytes_io = io.BytesIO(request.body) #request.body utf-8 编码的二进制文件

        try:
            sftp.putfo(bytes_io, exam_knowledge_path)
            print("上传成功")
        except Exception as e:
            # 这里处理文件传输过程中可能出现的错误
            print("文件传输错误：", str(e))
            return 'File transfer error'
        sftp.close()
        ssh.close()
        return JsonResponse({"result": "处理成功"})

    return JsonResponse({"result":"No POST error!"})


def LLM_preview(request, exam_id):

    print('LLM预览 从前端传回来的考试exam_id：',exam_id)

    exam = Exams.objects.filter(id=exam_id)[0]
    exam_path = exam.paper_identity_path

    ssh = ssh_connect()
    sftp = ssh.open_sftp()
    exam_data = sftp.file(exam_path, 'rb').read()

    tmp_path = os.path.join(settings.BASE_DIR,"server/.cache/tmp.docx")
    pdf_path=tmp_path.replace('docx','pdf')

    with open(tmp_path, 'wb') as local_file:
        local_file.write(exam_data)
        
    print('docx convert to pdf')
    convert(tmp_path, pdf_path)

    with fitz.open(pdf_path) as pdf:
        images=[]
        if isinstance(pdf,fitz.Document):
            for pg_i in range(pdf.page_count):

                matrix = fitz.Matrix(240/72, 240/72)
                pixmap = pdf[pg_i].get_pixmap(matrix=matrix ,alpha=False)         
                images.append(pixmap)

    images_base64 = [base64.b64encode(img.tobytes(output='jpg')).decode('utf-8') for img in images]

    sftp.close()
    ssh.close()
    os.remove(pdf_path)

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