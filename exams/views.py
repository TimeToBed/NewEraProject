from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import *  # assuming you have an Exam model
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core import serializers
import os
import json
import logging
import ast
from asgiref.sync import sync_to_async
from .ocr import ocr_getresult, ocr_jsonsave
logger = logging.getLogger(__name__)
from .LLM_package import *
import paramiko
from datetime import datetime
from demo import settings
from docx2pdf import convert
from django.db.models import Max
import posixpath

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
        for dir in [settings.Remote_path, str(max_id + 1), "papers"]:
            paper_path = posixpath.join(paper_path, dir)
            try:
                # 尝试切换到指定的目录
                sftp.chdir(paper_path)
            except FileNotFoundError:
                # 如果切换目录失败，说明目录不存在，我们在此创建目录
                print('create')
                
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

        sftp.close()
        exam = Exams(exam_name=exam_name, edate=edate, subject=subject, cdate=cdate, teacher_id=teacher_id, paper_identity_path=remote_paper_path, paper_answer_path=remote_result_path)
        exam.save()
    
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

def upload_package(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        exam_id = data.get('examid')
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
        for student_file in data['filelist']:
            student_id = student_file.get('studentid')
            i = 1
            for file in student_file['file']:
                pic_name = str(i) + '.png'
                i += 1
        paper = Papers.objects.get(exam_id=int(exam_id))
        uploaded_file = request.FILES['package']
        fs = OverwriteStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        package_url = fs.url(name)
        name = uploaded_file.name
        package_path = os.path.join('./media', name)  # 试卷图片路径
        return render(request, 'upload.html', locals())
async def test_p(p_test_problem):
    #可以直接将这两行代码放入指定位置，进行流式异步传输
    async for content in analysis_problem(p_test_problem):
        print(content, end="")

# from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


async def calculate_context(result):
    context = ""
    async for content in analysis_problem(result):
        context += content
    return context

#@csrf_exempt
async def rectangle(request):
    print('rectangle')
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


async def index_fun(request):
    # async for content in analysis_problem(p_test_problem):
    #     print(content, end="")
    return HttpResponse("Hello world ! ")

def examlist(request, user_id):
    
    print('从前端传回来的用户id：',user_id)
    exams = Exams.objects.filter(teacher_id=user_id)
    data = []
    cnt=1
    for exam in exams:
        markingable=False #判断能否批改
        """
        判断能不能批改，通过看是否上传了试卷
        """
        papers = Papers.objects.filter(exam_id=exam.id)
        if papers:
            markingable=True           
        data.append({'index':cnt,
                     'exam_id':exam.id,
                     'exam_name':exam.exam_name, 
                     'subject':exam.subject,
                     'markingable': markingable, 
                     'exam_date':exam.edate.strftime("%Y-%m-%d %H:%M:%S"),
                     'markingable': markingable})
        cnt+=1
    return JsonResponse(data, safe=False)


def paperlist(request, exam_id):
    
    print('从前端传回来的考试exam_id：',exam_id)
    # papers = Papers.objects.filter(exam_id=exam_id)
    papers = Papers.objects.filter(exam_id=exam_id)
    data = []
    cnt=1
    for paper in papers:
        data.append({'index': cnt,
                     'paper_id':paper.id,
                     'state':paper.state,
                     'pages':paper.pages, 
                     'student_id':paper.student_id,
                     'student_name':paper.student.user_name,
                     'ocr_preprocess':1,      #这里先假设为1，待修改
                    })
    cnt+=1
    # print(data)
    
    return JsonResponse(data, safe=False)
def ocr_preprocess(request, exam_id):
    print('OCR预处理 从前端传回来的考试exam_id：',exam_id)

    return HttpResponse("收到")


def LLM_preprocess(request, exam_id):
    print('LLM预处理 从前端传回来的考试exam_id：',exam_id)

    return HttpResponse("收到")

