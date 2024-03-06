

from django.contrib import admin
from django.urls import path,include
from . import views

app_name = 'exams'
urlpatterns = [
    #path('exams/', include("exams.urls")),
    path('upload/', views.upload_image, name='upload_image'),
    path('create_exam/', views.create_exam, name='create_exam'), #create_exam/
    path('upload/rectangle/', views.rectangle, name='rectangle'),
    path('examlist/<str:user_id>/', views.examlist),
    path('paperlist/<str:exam_id>/', views.paperlist),
    path('ocr_preprocess/<str:exam_id>/', views.ocr_preprocess),
    path('llm_preprocess/<str:exam_id>/', views.LLM_preprocess),
    path('llm_preview/<str:exam_id>/', views.LLM_preview),
    path('uploadpapers/<str:exam_id>/', views.upload_package)
    ]