# Generated by Django 4.2.10 on 2024-03-18 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exams", "0003_alter_exams_paper_answer_path_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="exams",
            name="fake_exam",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="students",
            name="fake_student",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="students",
            name="sno",
            field=models.IntegerField(default=6233112003),
        ),
        migrations.AddField(
            model_name="teachers",
            name="fake_teahcer",
            field=models.IntegerField(null=True),
        ),
    ]
