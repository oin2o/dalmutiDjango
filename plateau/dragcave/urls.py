from django.urls import path
from . import views

app_name = 'dragcave'

urlpatterns = [
    path('eggs', views.EggsView.as_view(), name='eggs'),
    path('abandoned', views.AbandonedView.as_view(), name='abandoned'),

]
