from django.urls import path
from . import views

app_name = 'liar'

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('category', views.CategoryView.as_view(), name='category'),
    path('word', views.WordView.as_view(), name='words'),
    path('word/<str:categoryname>', views.WordDetailView.as_view(), name='word'),
    path('<str:gamecode>/<str:username>', views.GameView.as_view(), name='game'),
    path('login/<str:gamecode>/', views.LoginView.as_view(), name='login'),
    path('telegram/<str:gamecode>/<str:username>', views.TelegramView.as_view(), name='telegram'),
]
