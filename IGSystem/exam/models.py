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