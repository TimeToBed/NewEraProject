from django.db import models
from django.core.validators import MinLengthValidator

"""
create database test; 创建数据库
alter database IMSystem character set utf8 collate utf8_general_ci; 更改数据库格式为中文(随时可以更改)
如果新建的表字符集不对可以在数据库插件中直接更改，如果已经加入了数据则更改字符集无效(此时需要新建表迁移数据)

CharField(blank=True)，
blank=True的设定告诉Django这个字段在表单验证时允许为空(用户如果没有为这个字段输入数据)。
null: 如果为 True，数据库中的该字段允许为空。
unique: 如果设置为 True，这个字段在整个数据表中必须是唯一的。
db_index: 如果为 True，为这个字段创建索引。
default: 为这个字段设置默认值。
verbose_name: 这是一个对人类友好的字段名，通常在 Django 的管理界面中显示。

my_instance = MyModel.objects.create(my_field=None) 为null的创建方式
"""
class Teams(models.Model):

    name = models.CharField(max_length=10)

    class Meta:
        db_table = 'Teams'
    
    def __str__(self):
        return self.name

class Teachers(models.Model):

    user_name = models.CharField(max_length=10) #教师用户名 必填
    password = models.CharField(max_length=30,validators=[MinLengthValidator(6)])  #教师密码 必填
    team = models.ForeignKey(Teams, models.DO_NOTHING, null=True)

    class Meta:
        db_table = 'Teachers'
    
    def __str__(self):
        return self.user_name

class Students(models.Model):

    id = models.IntegerField(primary_key=True)
    team = models.ForeignKey(Teams, models.DO_NOTHING, null=True)
    user_name = models.CharField(max_length=10)
    password = models.CharField(max_length=30,validators=[MinLengthValidator(6)])

    class Meta:
        db_table = 'Students'
    def __str__(self):
        return self.user_name


class Exams(models.Model):
    exam_name = models.CharField(max_length=40)    #考试名称 必填
    subject = models.CharField(max_length=20)   #考试科目 必填
    edate = models.DateTimeField()      #考试时间 创建时必填
    cdate = models.DateTimeField(auto_now=True)         #创建日期 自动创建

    llm_knowledge_path = models.CharField(max_length=100, null=True)  #大模型知识点总结json文件路径，非必填

    paper_identity_path = models.CharField(max_length=100)   #空白试卷 必填
    paper_answer_path = models.CharField(max_length=100, null=True)   #试卷答案 非必填

    teacher = models.ForeignKey(Teachers, models.CASCADE)  # 依附于教师，教师删除则依附教师的实例也删除

    class Meta:
        db_table = 'Exams'
    
    def __str__(self):
        return f'{self.exam_name}_{self.subject}'


class Papers(models.Model):

    exam = models.ForeignKey(Exams, models.CASCADE, null=True) #所依附的考试 创建时允许为空
    pic_path = models.CharField(max_length=100) #试卷图片路径  必填

    ocr_path = models.CharField(max_length=100, null=True) # ocr结果保存路径    非必填
    llm_result_path = models.CharField(max_length=100, null=True) #文心分析结果路径
    mark_result_path = models.CharField(max_length=100, null=True) #批改结果保存路径

    student = models.ForeignKey(Students, models.CASCADE, null=True) #所属学生
    cdate = models.DateTimeField(auto_now=True)         #创建日期 自动创建
    state = models.IntegerField(default=0)  # 0:未批阅 1：批阅中 2：已批阅
    pages = models.IntegerField()

    class Meta:
        db_table = 'Papers'
    
        