"""upfile URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from app.views import index
from app.views import case1
from app.views import case2
from app.views import case3
from app.views import case4
from app.views import case5
from app.views import case6
from app.views import case7
from app.views import case8

urlpatterns = [
    path('admin/', admin.site.urls),# 用不到可以不用寫
    path('index/', index),
    path('case1/', case1),
    path('case2/', case2),
    path('case3/', case3),
    path('case4/', case4),
    path('case5/', case5),
    path('case6/', case6),
    path('case7/', case7),
    path('case8/', case8),
    path('', index),
]
