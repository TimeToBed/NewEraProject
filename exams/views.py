from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import *  # assuming you have an Exam model
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, FileResponse, HttpResponse
from django.core import serializers
import os
import json
import ast
import io
import base64
from asgiref.sync import sync_to_async
from .ocr import *
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
import re       
import urllib.request
import numpy as np
from io import StringIO
json_dir = './server/ocr'
class OverwriteStorage(FileSystemStorage):
    def _save(self, name, content):
        if self.exists(name):
            os.remove(os.path.join(self.location, name))
        return super()._save(name, content)

    def get_available_name(self, name, max_length=None):
        return name

@csrf_exempt
def create_exam(request):
    if request.method == 'POST':
        exam_name = request.POST.get('examname')
        subject = request.POST.get('subject')
        edate = request.POST.get('time')
        cdate = timezone.now()
        teacher_id = request.POST.get('teacher_id') 
        paper = request.FILES.get('paper')
        result = request.FILES.get('result')
        
        max_id = Exams.objects.all().aggregate(Max('id'))
        if max_id['id__max'] is None:
            max_id = 0
        else:
            max_id = max_id['id__max']

        if exam_name=='':
            msg='名称不能为空！'
            return JsonResponse({'msg':msg})
        
        # 转化edate的格式
        edate = edate.rsplit(' ', 1)[0]
        edate = datetime.strptime(edate, '%a %b %d %Y %H:%M:%S %Z%z')
                
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
        # 考试卷在服务器的路径
        paper_name = exam_name + '_paper.docx'
        # paper_path = settings.Remote_path + str(max_id + 1) + '/' + "papers"
        paper_path = ''
        for dir in [settings.Remote_path, 'temp', "papers"]:
            paper_path = posixpath.join(paper_path, dir)
            try:
                # 尝试切换到指定的目录
                sftp.chdir(paper_path)
            except FileNotFoundError:
                # 如果切换目录失败，说明目录不存在，我们在此创建目录
                print('create')
                print(paper_path)
                sftp.mkdir(paper_path)
        remote_paper_path = paper_path + '/' + paper_name
        # 答案在服务器的路径
        if result:
            result_name = exam_name + '_answer.docx'
            remote_result_path = paper_path + '/' + result_name
            
        else:
            remote_result_path=None

        try:
            sftp.putfo(paper, remote_paper_path)
            if result:
                sftp.putfo(result, remote_result_path)
            print("上传成功")
        except Exception as e:
            # 这里处理文件传输过程中可能出现的错误
            print("文件传输错误：", str(e))
            return 'File transfer error'

        exam = Exams(exam_name=exam_name, edate=edate, subject=subject, cdate=cdate, teacher_id=teacher_id, paper_identity_path=remote_paper_path, paper_answer_path=remote_result_path)
        exam.save()
        
        before_paper_path = posixpath.join(settings.Remote_path, 'temp')
        new_paper_path = posixpath.join(settings.Remote_path, str(exam.id))
        sftp.rename(before_paper_path, new_paper_path)
        
        exam = Exams.objects.get(id=exam.id)
        paper_identity_path = posixpath.join(new_paper_path, 'papers', paper_name)
        paper_answer_path = posixpath.join(new_paper_path, 'papers', result_name)
        exam.paper_identity_path = paper_identity_path
        exam.paper_answer_path = paper_answer_path
        exam.save()
        
        sftp.close()
        ssh.close()
        
    return JsonResponse({'msg':'success'})


@csrf_exempt
def upload_image(request):
    #request.encoding='utf-8'
    if request.method == 'POST':
        uploaded_file = request.FILES['image']
        fs = OverwriteStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        image_url = fs.url(name)
        name = uploaded_file.name
        pic_path = os.path.join('./media', name)  # 试卷图片路径
        
        # 调用ocr识别图片并保存结果在数据库
        ocr_result, ocr_path =  ocr_getresult(pic_path, json_dir)
        print(ocr_path)
        name=name.replace(name.split('.')[-1],'json')
        #ocr_path = os.path.join('../server/ocr', name)  # 识别结果路径
        check_result_path = os.path.join('../server/result', name)  # 评阅内容路径
        exam_id=request.POST['exam_id']

        print(exam_id)
        # print('exam_id:',exam_id[-1])
        paper = Papers(exam_id=Exams.objects.get(id=int(exam_id)),pic_path = pic_path,ocr_path = ocr_path, check_result_path=check_result_path)

        paper.save()
        return render(request, 'upload.html', locals())
    return render(request, 'upload.html', locals())

def delete_remote_dir(sftp, remote_dir):
    for filename in sftp.listdir(remote_dir):
        filepath = remote_dir + '/' + filename
        sftp.remove(filepath)
    # 删除空目录
    sftp.rmdir(remote_dir)


@csrf_exempt
def upload_package(request, exam_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        # with open(r"E:\master\研一\服务外包\Untitled-2(1).json", "r", encoding='utf-8') as f:
        #     data = json.load(f)
        # data = json.loads(r"E:\master\研一\服务外包\Untitled-2(1).json")
        # exam_id = request.POST.get('exam_id')
        exam_id = data.get('exam_id')
        print(exam_id)
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
        students_papers = posixpath.join(settings.Remote_path, str(exam_id), 'student_papers')
        try:
            # 尝试切换到指定的目录
            sftp.chdir(students_papers)
        except FileNotFoundError:
            # 如果切换目录失败，说明目录不存在，我们在此创建目录
            print('create')
            sftp.mkdir(students_papers)
        for student_file in data['filelist']:
            student_id = student_file.get('filename')
            students_dir = posixpath.join(students_papers, str(student_id))
            try:
                sftp.stat(students_dir)
                delete_remote_dir(sftp, students_dir)
            except IOError:
                pass
            sftp.mkdir(students_dir)
            i = 1
            for file in student_file['file']:
                # print(file)
                pic_name = str(i) + '.png'
                file = re.sub(r'data:image/.+;base64,', '', file)
                file_data = base64.b64decode(file)  # Decode the Base64 string to bytes.
                file_obj = io.BytesIO(file_data)
                student_file = posixpath.join(students_dir, pic_name)
                try:
                    sftp.putfo(file_obj, student_file)
                    print("上传成功")
                except Exception as e:
                    # 这里处理文件传输过程中可能出现的错误
                    print("文件传输错误：", str(e))
                    return 'File transfer error'
                i += 1
            paper = Papers()
            paper.pic_path = students_dir
            paper.state = 0
            paper.pages = i - 1
            paper.exam_id = exam_id
            paper.student_id = student_id
            paper.save()
        
        sftp.close()
        ssh.close()
        
        return JsonResponse({'msg':'success'})
    


async def index_fun(request):
    # async for content in analysis_problem(p_test_problem):
    #     print(content, end="")
    return HttpResponse("Hello world ! ")

def examlist(request, user_id):
    
    # print('从前端传回来的用户id：',user_id)
    exams = Exams.objects.filter(teacher_id=user_id)
    data = []
    cnt=1
    for exam in exams:
        markingable=False #判断能否批改
        """
        判断能不能批改，通过看是否上传了试卷
        """
        if exam.llm_knowledge_path is not None:
            llm_preprocess = 1
        else:
            llm_preprocess = 0
        papers = Papers.objects.filter(exam_id=exam.id)
        if papers:
            markingable=True           
        data.append({'index':cnt,
                     'exam_id':exam.id,
                     'exam_name':exam.exam_name, 
                     'subject':exam.subject,
                     'markingable': markingable, 
                     'exam_date':exam.edate.strftime("%Y-%m-%d %H:%M:%S"),
                     'llm_preprocess':llm_preprocess
                     })
        cnt+=1
    return JsonResponse(data, safe=False)


def paperlist(request, exam_id):
    
    # print('从前端传回来的考试exam_id：',exam_id)
    # papers = Papers.objects.filter(exam_id=exam_id)
    papers = Papers.objects.filter(exam_id=exam_id)
    data = []
    cnt=1
    for paper in papers:
        if paper.ocr_path is not None:
            ocr_preprocess = 1
        else:
            ocr_preprocess = 0
        data.append({'index': cnt,
                     'paper_id':paper.id,
                     'state':paper.state,
                     'pages':paper.pages, 
                     'student_id':paper.student_id,
                     'student_name':paper.student.user_name,
                     'ocr_preprocess':ocr_preprocess,      #这里先假设为1，待修改
                    })
        cnt+=1
    # print(data)
    
    return JsonResponse(data, safe=False)


def ocr_preprocess(request, exam_id):
    print('OCR预处理 从前端传回来的考试exam_id：',exam_id)
    
    weights_path = get_weights_path()
    ocr = PaddleOCR(use_angle_cls=True, lang="ch",use_gpu=True,
 
                rec_model_dir= os.path.join(weights_path,'ch_PP-OCRv4_rec_infer'),
 
                cls_model_dir= os.path.join(weights_path,'ch_ppocr_mobile_v2.0_cls_infer'),
 
                det_model_dir= os.path.join(weights_path,'ch_PP-OCRv4_det_infer'))
    
    path = posixpath.join(settings.Remote_path, exam_id, 'student_papers')
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
    ocr_path = posixpath.join(settings.Remote_path, exam_id, 'ocr_result')
    try:
        # 尝试切换到指定的目录
        sftp.chdir(ocr_path)
    except FileNotFoundError:
        # 如果切换目录失败，说明目录不存在，我们在此创建目录
        print('create')
        sftp.mkdir(ocr_path)
                
    entries = sftp.listdir(path)
    for entry in entries:
        entry_path = posixpath.join(path, entry)
        # 如果这是一个文件夹
        if stat.S_ISDIR(sftp.stat(entry_path).st_mode):
            lenth = len(sftp.listdir(entry_path))
            i = 1
            while(i <= lenth):
                file = str(i) + '.jpg'
                file_path = posixpath.join(entry_path, file)
                # 如果条目是一个文件，将它添加到文件列表
                if not stat.S_ISDIR(sftp.stat(file_path).st_mode):
                    remote_file = sftp.open(file_path, 'rb')
                    # 转换图片到numpy数组
                    np_image = imageio.imread(BytesIO(remote_file.read()))
                    txt_path = posixpath.join(ocr_path, str(entry) + '.txt')
                    ocr_result = ocr.ocr(np_image, cls=True)
                    for idx in range(len(ocr_result)):
                        res = ocr_result[idx]
                        for line in res:
                            coords, contents, confidence = line[0], line[1][0], line[1][1]
                            with sftp.open(txt_path, 'ab') as f:
                                f.write(contents.encode('utf-8'))
                                f.write('\n'.encode('utf-8'))
                i += 1
            paper = Papers.objects.get(exam_id=exam_id, student_id=entry)
            paper.ocr_path = txt_path
            paper.save()
    
    sftp.close()
    ssh.close()
    
    return HttpResponse("收到")


def querypaper(request, paper_id):
    print('查询试卷 从前端传回来的考试paper_id：',paper_id)
    paper = Papers.objects.filter(id=paper_id)[0]
    print(paper)
    data={
        'msg':'hello world!'
        }
    exam_id=str(paper.exam_id)
    student_id=str(paper.student_id)
    print('exam id:', exam_id)
    paper_path = posixpath.join(settings.Remote_path, exam_id, 'student_papers',student_id)
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
    try:
        # 尝试切换到指定的目录
        sftp.chdir(paper_path)
    except FileNotFoundError:
        # 如果切换目录失败，说明目录不存在，我们在此创建目录
        print('Error for find:',paper_path)

    if stat.S_ISDIR(sftp.stat(paper_path).st_mode):
        length = len(sftp.listdir(paper_path))
        print("paper nums:", length)
        i = 1
        images=[]
        while(i <= length):
            file = str(i) + '.jpg'
            file_path = posixpath.join(paper_path, file)
            # 如果条目是一个文件，将它添加到文件列表
            if not stat.S_ISDIR(sftp.stat(file_path).st_mode):
                file_data = sftp.file(file_path, 'rb').read()
                image_bytes = io.BytesIO(file_data)
                images.append(image_bytes)
            i+=1
    images_base64 = [base64.b64encode(img.read()).decode('utf-8') for img in images]
    sftp.close()
    ssh.close()
    return JsonResponse(images_base64, safe=False)

#获取单张图片，试了一下，可以成功在前端显示
def querypaper_old2(request, paper_id):
    print('LLM预览 从前端传回来的考试paper_id：',paper_id)
    paper = Papers.objects.filter(id=paper_id)[0]
    print(paper)
    data={
        'msg':'hello world!'
        }
    exam_id=str(paper.exam_id)
    student_id=str(paper.student_id)
    print('exam id:', exam_id)
    paper_path = posixpath.join(settings.Remote_path, exam_id, 'student_papers',student_id)
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
    try:
        # 尝试切换到指定的目录
        sftp.chdir(paper_path)
    except FileNotFoundError:
        # 如果切换目录失败，说明目录不存在，我们在此创建目录
        print('Error for find:',paper_path)

    temp_dir = os.path.join(r'./server/cache/papers',exam_id, 'student_papers',student_id)#tempfile.mkdtemp()
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    if stat.S_ISDIR(sftp.stat(paper_path).st_mode):
        length = len(sftp.listdir(paper_path))
        print("paper nums:", length)
        i = 1
        while(i <= length):
            temp_file = tempfile.TemporaryFile()
            file = str(i) + '.jpg'
            file_path = posixpath.join(paper_path, file)
            # 如果条目是一个文件，将它添加到文件列表
            if not stat.S_ISDIR(sftp.stat(file_path).st_mode):
                remote_file = sftp.open(file_path, 'rb')
                temp_file.write(remote_file.read())
                temp_file.seek(0)
                # local_file_path = os.path.join(temp_dir, file)
                # with open(local_file_path, 'wb') as local_file:
                #     local_file.write(remote_file.read())
                print(i, 'remote file:', file_path)
            i+=1
            return FileResponse(temp_file, as_attachment=True, filename=file)
                # 转换图片到numpy数组
        #         np_image = imageio.imread(BytesIO(remote_file.read()))
        #         txt_path = posixpath.join(ocr_path, str(entry) + '.txt')
        #         ocr_result = ocr.ocr(np_image, cls=True)
        #         for idx in range(len(ocr_result)):
        #             res = ocr_result[idx]
        #             for line in res:
        #                 coords, contents, confidence = line[0], line[1][0], line[1][1]
        #                 with sftp.open(txt_path, 'ab') as f:
        #                     f.write(contents.encode('utf-8'))
        #                     f.write('\n'.encode('utf-8'))
        #     i += 1
        # paper = Papers.objects.get(exam_id=exam_id, student_id=entry)
        # paper.ocr_path = txt_path
        # paper.save()
    #shutil.make_archive(temp_dir, 'zip', temp_dir)
    #zip_file_path = temp_dir + '.zip'
    #response = FileResponse(open(zip_file_path, 'rb'))
    #response['Content-Disposition'] = 'attachment; filename="papers.zip"'
    #return response
    sftp.close()
    ssh.close()
    data['paper_path']=temp_dir
    return JsonResponse(data, safe=False)

# 将服务器的数据保存在本地的缓存目录
def querypaper_old(request, paper_id):
    print('LLM预览 从前端传回来的考试paper_id：',paper_id)
    paper = Papers.objects.filter(id=paper_id)[0]
    print(paper)
    data={
        'msg':'hello world!'
        }
    exam_id=str(paper.exam_id)
    student_id=str(paper.student_id)
    print('exam id:', exam_id)
    paper_path = posixpath.join(settings.Remote_path, exam_id, 'student_papers',student_id)
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
    try:
        # 尝试切换到指定的目录
        sftp.chdir(paper_path)
    except FileNotFoundError:
        # 如果切换目录失败，说明目录不存在，我们在此创建目录
        print('Error for find:',paper_path)

    temp_dir = os.path.join(r'./server/cache/papers',exam_id, 'student_papers',student_id)#tempfile.mkdtemp()
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    else:  #如果缓存文件中已经有了，就不需要再拉取了
        return JsonResponse(data, safe=False)
    if stat.S_ISDIR(sftp.stat(paper_path).st_mode):
        length = len(sftp.listdir(paper_path))
        print("paper nums:", length)
        i = 1
        while(i <= length):
            file = str(i) + '.jpg'
            file_path = posixpath.join(paper_path, file)
            # 如果条目是一个文件，将它添加到文件列表
            if not stat.S_ISDIR(sftp.stat(file_path).st_mode):
                remote_file = sftp.open(file_path, 'rb')
                local_file_path = os.path.join(temp_dir, file)
                with open(local_file_path, 'wb') as local_file:
                    local_file.write(remote_file.read())
                print(i, 'remote file:', file_path)
            i+=1
             
    sftp.close()
    ssh.close()
    data['paper_path']=temp_dir
    return JsonResponse(data, safe=False)

def remove_all(sftp, remote_dir_path):
    # 获取remote_dir_path下所有文件和文件夹
    for entry in sftp.listdir_attr(remote_dir_path):
        # 拼接全路径
        path = posixpath.join(remote_dir_path, entry.filename)
        # 如果是个文件夹，则递归删除
        if stat.S_ISDIR(entry.st_mode):
            remove_all(sftp, path)
        else:
            # 否则尝试删除文件
            sftp.remove(path)
    # 最后删除主文件夹
    sftp.rmdir(remote_dir_path)
    
def delete_exam(request, exam_id):
    paper = Papers.objects.filter(exam_id=exam_id)
    if paper.exists():
        paper.delete()
    exam = Exams.objects.filter(id=exam_id)
    if exam.exists():
        exam.delete()
    remote_dir_path = posixpath.join(settings.Remote_path, exam_id)
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
    remove_all(sftp, remote_dir_path)
    sftp.close()
    ssh.close()
    return JsonResponse({'msg':'success'})

@csrf_exempt
def fake1(request):
    if request.method == 'POST':
        num = request.POST.get('number')
        print("一键生成指定数量学生的 数据", num)
        num = int(num)
        for i in range(num):
            student = Students.objects.create(
                user_name='student'+str(i),
                password='123456',
                fake_student=1,
                sno = 6233112003 + i
            )

@csrf_exempt
def fake2(request):
    if request.method == 'POST':
        begin_time = request.POST.get('startdate')
        end_time = request.POST.get('enddate')
        isinterval=request.POST.get('isinterval')
        num=request.POST.get('number')
        print("批量生成考试", begin_time, end_time, isinterval, num)
        isinterval = int(isinterval)
        num = int(num)
        res = end_time - begin_time
        res_days = res.days
        max_id = Exams.objects.all().aggregate(Max('id'))
        if max_id['id__max'] is None:
            max_id = 0
        else:
            max_id = max_id['id__max']
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
        for i in range(num):
            exam_path = posixpath.join(settings.Remote_path, str(max_id + i))
            try:
                # 尝试切换到指定的目录
                sftp.chdir(exam_path)
            except FileNotFoundError:
                # 如果切换目录失败，说明目录不存在，我们在此创建目录
                sftp.mkdir(exam_path)
            
            paper_path = posixpath.join(exam_path, 'papers')
            try:
                # 尝试切换到指定的目录
                sftp.chdir(paper_path)
            except FileNotFoundError:
                # 如果切换目录失败，说明目录不存在，我们在此创建目录
                sftp.mkdir(paper_path)
            
            before_paper_answer_path = r'/hdd/server/1010/papers/语文第一次月考_answer.docx'
            
            before_paper_identity_path = r'/hdd/server/1010/papers/语文第一次月考_paper.docx'
            #复制before_paper_identity_path到paper_identity_path
            with sftp.open(before_paper_answer_path, 'rb') as file_remote:
                file_content = file_remote.read()  # 读取远程文件内容
            
            paper_answer_path = posixpath.join(paper_path, '语文第一次月考_answer.docx')
            with sftp.open(paper_answer_path, 'wb') as file_target:
                file_target.write(file_content)
                
            
            with sftp.open(before_paper_identity_path, 'rb') as file_remote:
                file_content = file_remote.read()  # 读取远程文件内容
            
            paper_identity_path = posixpath.join(paper_path, '语文第一次月考_identity.docx')
            with sftp.open(paper_identity_path, 'wb') as file_target:
                file_target.write(file_content)
            
            if isinterval == 0:
                time = begin_time + timezone.timedelta(days=np.random.randint(0, res_days))
            else:
                time = begin_time + timezone.timedelta(days=i * (res_days // num))
            exam = Exams.objects.create(
                exam_name= f'{time.year}年{time.month}月语文考试',
                subject='语文',
                edate = time,
                cdate = time,
                paper_identity_path=paper_identity_path,
                paper_answer_path=paper_answer_path,
                teacher_id=1,
                fake_exam=1,
            )
        
        sftp.close()
        ssh.close()
        return JsonResponse({'msg':'success'})

def generate_paper():
    llm_first = ["请确保仔细理解和解读文章的上下文，这在寻找答案时是非常重要的。",
                 "尝试更好的把握和理解文章的关键词，这有助于你抓住文章的要点并回答问题。",
                 "需要进一步提高你对文章主旨理解的准确性，这对于阅读理解的成功至关重要。",
                 "注意文章的结构和组织，看看作者如何建立他们的论点，这可以帮助你更好的理解和解释文章。",
                 "清楚概括文章的主题和主旨，并正确解读文章的含义。",
                 "阅读的时候注意引用文献的信息，这不仅可以帮助理解文章，同时也有助于你了解作者对特定主题的观点。",
                 "你在解读作者观点上做得很好，但是需要在理解具体细节上下更多功夫。",
                 "在阅读时，要与自己的知识结构联系起来，理解新的信息，并思考它如何与你已经知道的信息相适应。"]
    llm_second = ["请注意积累并理解古代文体和词汇的用法，这将有助于你更好地理解并解析文本。",
                  "尝试从历史和文化背景的视角去阅读和理解文本，这对于你真正理解作品的含义尤为关键。",
                  "需要进一步提高你对文本主旨概念的理解，以便能够精准地捕捉到作者的意图和思想。",
                  "注意掌握和理解文章的句式结构和修辞技巧，这会帮你更好地理解作者的表达手法和意图。",
                  "在阅读文本时，要了解和联系上下文，这将帮助你更全面地理解文本及其作者的观点和意图。"]
    llm_sixteen = ["注意对古诗词的积累", "平时需要多背诵古诗词", "古诗词积累过少"]
    llm_third = ["在理解和使用短语或表达时，要注意其上下文含义，以确保其用法正确。",
                 "你需要更多地联系实际情境和文化背景，以提高你在语言运用中的适应性。",
                 "在分析和解释语言现象时，注意从更大的语境和背景考虑，这将帮助你更深入地理解和解释。",
                 "在阅读和理解文本时，注意运用你对语言和文化的知识，以提高你的理解力和鉴赏力。"]
    llm_forth = ["结构清晰，主题明确，需要在句子连贯性和逻辑结构上进一步加强。",
                 "篇章有序，逻辑清晰，但在语言修辞和词汇使用上需要更加精细化。",
                 "注意联系实际，将所学知识与生活世界紧密结合，以提高论证的说服力。",
                 "词汇丰富，语言流畅，注意在论据选择和展开上进一步细化。",
                 "注意积累篇章结构和语言表达，这将有助于你的写作水平的提高。",
                 "注重开头和结尾的创新，使文章更加有吸引力和感染力。",
                 "在阐述观点时，尽量多角度考虑问题，表达更为全面和深入。",
                 "在撰写过程中，注意巧妙运用修辞，增强语言的表现力。"]

    teacher_first = ["在理解文本时，可以尝试总结每个段落的主要观点，这将有助于你提高阅读效率和理解力。",
                     "你已经很好地理解了文本的大意，希望你能在理解上下文和作者的意图上再下一番功夫。",
                     "建议你在阅读时注意作者的语言和风格，这将加深你对文本的理解。",
                     "你的答卷显示出对文本理解的一致性，再进行一些关于作者意图的深入分析，会更出色哦。"]
    teacher_second = [
        "很高兴看到你对文本进行了深入的分析。掌握更多的词汇并理解它们在古代语境中的含义，将有助于你更精确地理解和解读文本。",
        "你已经具备了理解古代文本的基本能力，希望你能再进一步，探索作者的创作动机和心境，这将使你的理解更为深入。",
        "你在回答问题的过程中很直接，提供了精准的信息，试着进一步解析或者链接到文本中的其他内容。"]
    teacher_sixteen = ["平常记得多积累古诗词啊。", "在背诵方面还需要花时间。"]
    teacher_third = ["你已展示出了扎实的语言基础，继续在熟悉语法规则和扩大词汇量上努力，将使你的语言运用能力更上一层楼。",
                     "你已经展现出对语言文字运用的基本掌握，但在理解和使用一些高级语法结构时还需要进一步的练习。",
                     "适当的拓展和丰富你的表述将更加显示出你的语言运用技巧。"]
    teacher_forth = [
        "你在文字运用上已经表现得很好了，我很高兴。不过，记住，总体定语和定语从句的使用可以增加你的句子的丰富性，这对于提高你的写作技巧而言非常有帮助。",
        "我欣赏你在答题中准确使用词汇的能力，这体现出你已经了解和掌握了这些词汇。在接下来的学习中，我希望你能够尝试更丰富、更具挑战性的词汇和表达方式。",
        "我注意到你在文字运用上的强项，那就是你的表达清晰易懂。不过，使用一些修辞手法，如比喻，夸张，可以使你的表达更生动，更富有表现力。"]
    with open(r"C:\Users\16338\Downloads\paper_mark_result.json", "rb") as f:
        file_content = json.load(f)

    for i in range(1, 4):
        seed = np.random.randint(0, 2)
        if seed < 0.5:
            file_content['一']['（一）'][f'{i}']['llm_mark'] = seed * 3
            file_content['一']['（一）'][f'{i}']['mark_score'] = seed * 3
            file_content['一']['（一）'][f'{i}']['llm_comment'] = np.random.choice(llm_first, 1)[0]
            file_content['一']['（一）'][f'{i}']['comment'] = np.random.choice(teacher_first, 1)[0]
        else:
            file_content['一']['（一）'][f'{i}']['llm_mark'] = seed * 3
            file_content['一']['（一）'][f'{i}']['mark_score'] = seed * 3

    for i in range(4, 7):
        seed = np.random.randint(0, 2)
        if seed < 0.4:
            file_content['一']['（二）'][f'{i}']['llm_mark'] = seed * 3
            file_content['一']['（二）'][f'{i}']['mark_score'] = seed * 3
            file_content['一']['（二）'][f'{i}']['llm_comment'] = np.random.choice(llm_first, 1)[0]
            file_content['一']['（二）'][f'{i}']['comment'] = np.random.choice(teacher_first, 1)[0]
        else:
            file_content['一']['（二）'][f'{i}']['llm_mark'] = seed * 3
            file_content['一']['（二）'][f'{i}']['mark_score'] = seed * 3

    for i in range(7, 10):
        seed = np.random.randint(0, 2)
        if seed < 0.6:
            file_content['一']['（三）'][f'{i}']['llm_mark'] = seed * 3
            file_content['一']['（三）'][f'{i}']['mark_score'] = seed * 3
            file_content['一']['（三）'][f'{i}']['llm_comment'] = np.random.choice(llm_first, 1)[0]
            file_content['一']['（三）'][f'{i}']['comment'] = np.random.choice(teacher_first, 1)[0]
        else:
            file_content['一']['（三）'][f'{i}']['llm_mark'] = seed * 3
            file_content['一']['（三）'][f'{i}']['mark_score'] = seed * 3

    for i in range(10, 13):
        seed = np.random.randint(0, 2)
        if seed < 0.3:
            file_content['二']['（一）'][f'{i}']['llm_mark'] = seed * 3
            file_content['二']['（一）'][f'{i}']['mark_score'] = seed * 3
            file_content['二']['（一）'][f'{i}']['llm_comment'] = np.random.choice(llm_second, 1)[0]
            file_content['二']['（一）'][f'{i}']['comment'] = np.random.choice(teacher_second, 1)[0]
        else:
            file_content['二']['（一）'][f'{i}']['llm_mark'] = seed * 3
            file_content['二']['（一）'][f'{i}']['mark_score'] = seed * 3
    for i in range(1, 3):
        seed = np.random.rand()
        seed2 = np.random.uniform(-0.2,0.2)
        file_content['二']['（一）']['13'][f'({i})']['llm_mark'] = min(int(seed * 5),5)
        file_content['二']['（一）']['13'][f'({i})']['mark_score'] = min(int((seed + seed2) * 5),5)
        file_content['二']['（一）']['13'][f'({i})']['llm_comment'] = np.random.choice(llm_second, 1)[0]
        file_content['二']['（一）']['13'][f'({i})']['comment'] = np.random.choice(teacher_second, 1)[0]
        if min(int(seed * 5),5) == 5:
            file_content['二']['（一）']['13'][f'({i})']['llm_comment'] = ''
        if min(int((seed + seed2) * 5),5) == 5:
            file_content['二']['（一）']['13'][f'({i})']['comment'] = ''

    for i in range(14, 16):
        seed = np.random.rand()
        if seed < 0.5:
            file_content['二']['（二）'][f'{i}']['llm_mark'] = seed * 3
            file_content['二']['（二）'][f'{i}']['mark_score'] = seed * 3
            file_content['二']['（二）'][f'{i}']['llm_comment'] = np.random.choice(llm_second, 1)[0]
            file_content['二']['（二）'][f'{i}']['comment'] = np.random.choice(teacher_second, 1)[0]
        else:
            file_content['二']['（二）'][f'{i}']['llm_mark'] = 3
            file_content['二']['（二）'][f'{i}']['mark_score'] = 3

    for i in range(1, 4):
        seed = np.random.rand()
        if seed < 0.5:
            file_content['二']['（三）']['16'][f'({i})']['llm_mark'] = 0
            file_content['二']['（三）']['16'][f'({i})']['mark_score'] = 0
            file_content['二']['（三）']['16'][f'({i})']['llm_comment'] = np.random.choice(llm_sixteen, 1)[0]
            file_content['二']['（三）']['16'][f'({i})']['comment'] = np.random.choice(teacher_sixteen, 1)[0]
        else:
            file_content['二']['（三）']['16'][f'({i})']['llm_mark'] = 2
            file_content['二']['（三）']['16'][f'({i})']['mark_score'] = 2

    for i in range(17, 20):
        seed = np.random.rand()
        if seed < 0.5:
            file_content['三'][f'{i}']['llm_mark'] = 0
            file_content['三'][f'{i}']['mark_score'] = 0
            file_content['三'][f'{i}']['llm_comment'] = np.random.choice(llm_third, 1)[0]
            file_content['三'][f'{i}']['comment'] = np.random.choice(teacher_third, 1)[0]
        else:
            file_content['三'][f'{i}']['llm_mark'] = 3
            file_content['三'][f'{i}']['mark_score'] = 3

    for i in range(20,22):
        seed = np.random.rand()
        seed2 = np.random.uniform(-0.2, 0.2)
        file_content['三'][f'{i}']['llm_mark'] = min(int(seed * 5), 5)
        file_content['三'][f'{i}']['mark_score'] = min(int((seed + seed2) * 5), 5)
        file_content['三'][f'{i}']['llm_comment'] = np.random.choice(llm_second, 1)[0]
        file_content['三'][f'{i}']['comment'] = np.random.choice(teacher_second, 1)[0]
        if min(int(seed * 5), 5) == 5:
            file_content['二']['（一）']['13'][f'({i})']['llm_comment'] = ''
        if min(int((seed + seed2) * 5), 5) == 5:
            file_content['二']['（一）']['13'][f'({i})']['comment'] = ''

    seed = np.random.rand()
    seed2 = np.random.uniform(-0.2, 0.2)
    print(min(int(seed * 60), 60))
    file_content['四']['22']['llm_mark'] = min(int(seed * 60), 60)
    file_content['四']['22']['mark_score'] = min(int((seed + seed2) * 60), 60)
    file_content['四']['22']['llm_comment'] = np.random.choice(llm_forth, 1)[0]
    file_content['四']['22']['comment'] = np.random.choice(teacher_forth, 1)[0]
    if min(int(seed * 60), 60) == 60:
        file_content['四']['22']['llm_comment'] = ''
    if min(int((seed + seed2) * 60), 60) == 60:
        file_content['四']['22']['comment'] = ''

    return file_content
    
@csrf_exempt
def fake3(request):
    if request.method == 'POST':
        exam_id = request.POST.get('exam_id')
        num = request.POST.get('number')
        
        num = int(num)
        student_paper_path = posixpath.join(settings.Remote_path, exam_id, 'student_papers')
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
        # 获取所有学生的QuerySet对象
        students = Students.objects.all()
        # 提取所有学生的id
        student_ids = [student.id for student in students]
    
        sftp = ssh.open_sftp()
        for i in range(num):
            student_id = np.random.choice(student_ids)
            student_dir = posixpath.join(student_paper_path, str(student_id))
            try:
                # 尝试切换到指定的目录
                sftp.chdir(student_dir)
            except FileNotFoundError:
                # 如果切换目录失败，说明目录不存在，我们在此创建目录
                sftp.mkdir(student_dir)
            file = generate_paper()
            data_str = json.dumps(file)
            data_io = StringIO(data_str)
            file_path = posixpath.join(student_dir, f'llm.json')
            sftp.putfo(data_io, file_path)  # 上传StringIO到远程服务器
            paper = Papers.objects.create(
                exam_id=exam_id,
                student_id=student_id,
                state=1,
                pages=12,
                cdate=timezone.now(),
                pic_path=student_dir,
                mark_result_path=file_path,
                fake_paper=1
            )
        sftp.close()
        ssh.close()
        return JsonResponse({'msg':'success'})

def fake4(request):
    print("一键删除所有fake数据")
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
    paper = Papers.objects.filter(fake_paper=1)
    paper.delete()
    exam = Exams.objects.filter(fake_exam=1)
    for i in exam:
        exam_id = i.id
        dir_path = posixpath.join(settings.Remote_path, str(exam_id))
        remove_all(sftp,dir_path)
    exam.delete()
    student = Students.objects.filter(fake_student=1)
    student.delete()
    sftp.close()
    ssh.close()
    return JsonResponse({'msg':'success'})
        

