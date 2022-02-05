"""plateau URL Configuration

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
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dalmuti/', include('dalmuti.urls')),
    path('dalmutip/', include('dalmutip.urls')),
    path('dalmutid/', include('dalmutid.urls')),
    path('lotto/', include('lotto.urls')),
    path('liar/', include('liar.urls')),
    path('davinci/', include('davinci.urls')),
    path('dixit/', include('dixit.urls')),
    path('dragcave/', include('dragcave.urls')),
    path('mongdang/', include('mongdang.urls')),
]
