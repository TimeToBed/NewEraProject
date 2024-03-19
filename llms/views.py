
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
import fitz,io,shutil

from datetime import datetime
from .models import *  # assuming you have an Exam model
from exams.models import *
from .LLM_package import *
# Create your views here.

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

    try:
        exam = Exams.objects.get(id=exam_id)
        exam_path = exam.paper_identity_path
        exam_answer_path = exam.paper_answer_path

    except Exams.DoesNotExist:
        return JsonResponse({"result":f"No exist {exam_id}!"})

    ssh = ssh_connect()
    sftp = ssh.open_sftp()

    if exam.llm_knowledge_path is not None:

        exam_analysis_path = exam.llm_knowledge_path
        print(f"{exam_analysis_path} already exists.")

    else:
        
        tmp_exam_path = os.path.join(settings.TEMP_URL,"exam_tmp.docx")
        tmp_answer_path = os.path.join(settings.TEMP_URL,"answer_tmp.docx")
        tmp_json_path = os.path.join(settings.TEMP_URL,"tmp.json")
        temp_kdb_path = os.path.join(settings.TEMP_URL,"knowledge")

        sftp.get(exam_path, tmp_exam_path)
        sftp.get(exam_answer_path, tmp_answer_path)
        print("开始预处理试卷...")

        pre_exam(tmp_exam_path, tmp_answer_path, tmp_json_path, temp_kdb_path)

        print("调用文心一言大模型进行分析...")
        print(os.environ.get("EB_AGENT_ACCESS_TOKEN"))
        asyncio.run(llm_analysis_exam(tmp_json_path,tmp_json_path))

        #保存知识分析路径
        exam_analysis_path = os.path.splitext(exam_path)[0] + '.json'
        sftp.put(tmp_json_path, exam_analysis_path)

        print("文件上传成功！")
        exam.llm_knowledge_path = exam_analysis_path
        exam.save() 

    with sftp.file(exam_analysis_path, 'rb',) as f:  # 打开远程服务器上的JSON文件
        exam_detail_info = json.loads(f.read().decode('utf-8'))  # 读取文件内容并解析为Python数据结构
    
    del_object(sftp,ssh)
    clean_server_cache()
    return JsonResponse(exam_detail_info, safe=False)

@csrf_exempt #保存llm修改
def LLM_update(request:HttpRequest, exam_id):

    print('LLM_update 从前端传回来的考试exam_id：',exam_id)
    try:
        exam = Exams.objects.get(id=exam_id)
        exam_knowledge_path = exam.llm_knowledge_path

    except Exams.DoesNotExist:
        return JsonResponse({"result":f"No exist {exam_id}!"})
  
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

    return JsonResponse({"result":"No Post error!"})


def LLM_preview2(request, exam_id):

    print('LLM预览 从前端传回来的考试exam_id：',exam_id)

    try:
        exam = Exams.objects.get(id=exam_id)
        exam_path = exam.paper_identity_path

    except Exams.DoesNotExist:
        return JsonResponse({"result":f"No exist id {exam_id}!"})

    ssh = ssh_connect()
    sftp = ssh.open_sftp()
    
    pdf_path = exam_path.replace('docx','pdf')
    tmp_doc_path = os.path.join(settings.TEMP_URL,"tmp.docx")
    tmp_pdf_path = os.path.join(settings.TEMP_URL,"tmp.pdf")
    print(pdf_path)

    try:
        sftp.stat(pdf_path)
        sftp.get(pdf_path, tmp_pdf_path)

        print(f"{pdf_path} already exists.")
    except IOError:

        sftp.get(exam_path, tmp_doc_path)
        print('docx 转换至 pdf')
        convert(tmp_doc_path, tmp_pdf_path)
        print(f'传送 pdf 至服务器: {pdf_path}')
        with open(tmp_pdf_path, 'rb') as f:  # 使用二进制模式打开本地PDF文件
            sftp.putfo(f, pdf_path)  # 上传PDF文件到服务器 


    with fitz.open(tmp_pdf_path) as pdf:
        images=[]
        if isinstance(pdf,fitz.Document):
            for pg_i in range(pdf.page_count):

                matrix = fitz.Matrix(300/72, 300/72)
                pixmap = pdf[pg_i].get_pixmap(matrix=matrix ,alpha=False)         
                images.append(pixmap)

    images_base64 = [base64.b64encode(img.tobytes(output='jpg')).decode('utf-8') for img in images]

    del_object(ssh, sftp)
    clean_server_cache()

    return JsonResponse(images_base64, safe=False)

def LLM_preview(request, exam_id):

    print('LLM预览 从前端传回来的考试exam_id：',exam_id)

    try:
        exam = Exams.objects.get(id=exam_id)
        exam_path = exam.paper_identity_path

    except Exams.DoesNotExist:
        return JsonResponse({"result":f"No exist id {exam_id}!"})

    ssh = ssh_connect()
    sftp = ssh.open_sftp()

    remote_file = sftp.open(exam_path, 'rb')
  
    # 创建一个FileResponse对象
    response = FileResponse(remote_file, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

    return response


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
        #async for content in analysis_problem(result):
        #    context+=content
        #    print(content, end="")
            

        # return JsonResponse({'status': 'ok', 'message': 'Data received.'})
        return JsonResponse({'status': 'ok', 'message': 'Data received.', 'result':context}) 
    return JsonResponse({'status': 'false', 'message': 'Error.'})
    #return await HttpResponse("Hello world ! ")