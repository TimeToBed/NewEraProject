from django.contrib import admin
from django.urls import path,include
from . import views

app_name = 'llms'
urlpatterns = [
    #path('exams/', include("exams.urls")),
    path('llm_preprocess/<str:exam_id>/', views.LLM_preprocess),
    path('llm_preview/<str:exam_id>/', views.LLM_preview),
    path('upload/rectangle/', views.rectangle, name='rectangle'),
    ]