# Generated by Django 3.2 on 2024-01-21 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('time', models.DateField()),
            ],
            options={
                'db_table': 'score',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('idstudent', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=45)),
                ('class_field', models.CharField(db_column='class', max_length=45)),
                ('sex', models.CharField(max_length=45)),
                ('age', models.IntegerField()),
                ('telephone', models.CharField(max_length=45)),
                ('father_name', models.CharField(max_length=45)),
                ('father_telephone', models.CharField(max_length=45)),
                ('mother_name', models.CharField(max_length=45)),
                ('mother_telephone', models.CharField(max_length=45)),
                ('address', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'student',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('idsubject', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('subject_name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'subject',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('idteacher', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=45)),
                ('sex', models.CharField(max_length=45)),
                ('age', models.IntegerField()),
                ('telephone', models.CharField(max_length=45)),
                ('address', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'teacher',
                'managed': False,
            },
        ),
    ]
