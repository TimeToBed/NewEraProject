# Generated by Django 4.2.10 on 2024-03-12 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exams", "0002_papers_score"),
    ]

    operations = [
        migrations.AlterField(
            model_name="exams",
            name="paper_answer_path",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="exams",
            name="paper_identity_path",
            field=models.CharField(max_length=100),
        ),
    ]
