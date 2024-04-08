
from django.contrib import admin
from django.urls import path,include
from . import views

app_name = 'exams'
urlpatterns = [
    #path('exams/', include("exams.urls")),
    path('upload/', views.upload_image, name='upload_image'),
    path('create_exam/', views.create_exam, name='create_exam'), #create_exam/
    path('examlist/<str:user_id>/', views.examlist),
    path('paperlist/<str:exam_id>/', views.paperlist),
    path('ocr_preprocess/<str:exam_id>/', views.ocr_preprocess),
    path('uploadpapers/<str:exam_id>/', views.upload_package),
    path('querypaper/<str:paper_id>/', views.querypaper),
    path('queryllm/<str:paper_id>/', views.queryllm),
    path('delete_exam/<str:exam_id>/', views.delete_exam),
    path('data_list/<str:teacher_id>/', views.data_list),
    path('marking_update/<str:paper_id>/', views.marking_update),
    path('update_paper_state/<str:paper_id>/', views.update_paper_state),
    path('fake1/', views.fake1),
    path('fake2/', views.fake2),
    path('fake3/', views.fake3),
    path('fake4/', views.fake4),
    path('login/', views.login),
    path('comment/', views.comment),
    path('data_list_app/<str:student_id>', views.data_list_app)
    ]