from django.db import models

class Exam(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    subject = models.CharField(max_length=20)
    edate = models.DateTimeField()
    cdate = models.DateTimeField()

    class Meta:
        db_table = 'exams'  
    def __str__(self):
        return self.id#f"{self.edate}-{self.name}-{self.subject}"

class Papers(models.Model):
    paper_no = models.AutoField(primary_key=True)  # 编号
    exam_id= models.ForeignKey(Exam, on_delete=models.CASCADE, db_column = 'exam_id')
    pic_path = models.CharField(max_length=100)  # 试卷图片路径
    ocr_path = models.CharField(max_length=100)  # 识别结果路径
    check_result_path = models.CharField(max_length=100)  # 评阅内容路径

    class Meta:
        db_table = 'papers'  # 指定数据库中的表名

class Score(models.Model):
    idsubject = models.ForeignKey('Subject', models.DO_NOTHING, db_column='idsubject')
    idstudent = models.ForeignKey('Student', models.DO_NOTHING, db_column='idstudent')
    score = models.IntegerField()
    time = models.DateField()

    class Meta:
        managed = False
        db_table = 'score'


class Student(models.Model):
    idstudent = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=45)
    class_field = models.CharField(db_column='class', max_length=45)  # Field renamed because it was a Python reserved word.
    sex = models.CharField(max_length=45)
    age = models.IntegerField()
    telephone = models.CharField(max_length=45)
    father_name = models.CharField(max_length=45)
    father_telephone = models.CharField(max_length=45)
    mother_name = models.CharField(max_length=45)
    mother_telephone = models.CharField(max_length=45)
    address = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'student'


class Subject(models.Model):
    idsubject = models.CharField(primary_key=True, max_length=45)
    subject_name = models.CharField(max_length=45)
    idteacher = models.ForeignKey('Teacher', models.DO_NOTHING, db_column='idteacher')

    class Meta:
        managed = False
        db_table = 'subject'


class Teacher(models.Model):
    idteacher = models.CharField(primary_key=True, max_length=45)
    name = models.CharField(max_length=45)
    sex = models.CharField(max_length=45)
    age = models.IntegerField()
    telephone = models.CharField(max_length=45)
    address = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'teacher'