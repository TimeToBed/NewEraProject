"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
#from upload import views
from django.conf.urls.static import static
from demo import settings
import exam.views
from .views import home, index

urlpatterns = [
    path('', home, name='home'),
    path('index/', index, name='index'),
    path('admin/', admin.site.urls),
    path('upload/', exam.views.upload_image, name='upload_image'),
    #path('', upload.views.upload_image, name='upload_image'),
    path('create_exam/', exam.views.create_exam, name='create_exam'),
    path('upload/rectangle/', exam.views.rectangle, name='rectangle'),
]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
