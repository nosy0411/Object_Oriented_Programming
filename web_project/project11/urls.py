"""project11 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
# include : 프로젝트 내에 속해 있는 application의 urls.py 파일을 그대로 가져와서 하위 경로로 사용하기 위한 모듈
from django.urls import include, path

urlpatterns = [
  # polls/ 하위 경로의 경우 polls application의 urls의 정의를 가져와서 사용함
  path('admin/', admin.site.urls),
  path('board/', include('Board.urls')),
  path('', include('User.urls')),
  path('',include('Report.urls')),
]
