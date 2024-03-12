from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import *  # assuming you have an Exam model
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, FileResponse
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
        paper_name = exam_name + '_paper.doc'
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
            result_name = exam_name + '_answer.doc'
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
                # 尝试切换到指定的目录
                sftp.chdir(students_dir)
            except FileNotFoundError:
                # 如果切换目录失败，说明目录不存在，我们在此创建目录
                print('create')
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


# word直接转图片，有水印
def LLM_preview_old(request, exam_id):
    from docx2pdf import convert
    import spire.doc as doc
    import spire.doc.common as common

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
    convert(tmppath, pdfpath)
    
    # 创建一个 Document 对象
    document = doc.Document()
    # 加载一个 Word DOCX 文件
    document.LoadFromFile(tmppath)

    # for section in document.Sections:
    #     for paragraph in section.paragraphs:
    #         for run in paragraph.runs:
    #             if "Evaluation Warning: the document was create with Spire.Doc for Python" in run.text:
    #                 paragraph.remove(run)

    image_streams = document.SaveImageToStreams(doc.ImageType.Bitmap)
    images_base64 = [base64.b64encode(img.ToArray()).decode('utf-8') for img in image_streams]

    
    sftp.close()
    ssh.close()
    document.Close()

    os.remove(tmppath)
    return JsonResponse(images_base64, safe=False)

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