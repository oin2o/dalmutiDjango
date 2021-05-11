from django.urls import path
from . import views

app_name = 'liar'

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('category', views.CategoryView.as_view(), name='category'),
    path('category/<str:categoryname>', views.GameView.as_view(), name='game'),
    path('word', views.WordView.as_view(), name='word'),
    path('word/<str:categoryname>', views.WordDetailView.as_view(), name='add'),
]
