"""MyProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from MyProject import views
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from login import views


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^index/', views.index),
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    url(r'^logout/', views.logout),
    url(r'^captcha', include('captcha.urls')),                 # 增加这一行
    url(r'^confirm/$', views.user_confirm),

    # path(r'hello/$',views.hello)
    # path('app01/', include('app01.urls')),
    path('app01/', include('app01.urls')),  # 转到app01

    path('analyse/', include('analyse.urls')),  # 转到analyse

]
