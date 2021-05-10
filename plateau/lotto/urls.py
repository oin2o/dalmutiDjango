from django.urls import path
from . import views

app_name = 'lotto'

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
]
