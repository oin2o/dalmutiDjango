from django.urls import path
from . import views

app_name = 'davinci'

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('rule', views.RuleView.as_view(), name='rule'),
    path('<str:gamecode>/<str:username>', views.GameView.as_view(), name='game'),
    path('login/<str:gamecode>/', views.LoginView.as_view(), name='login'),
    path('telegram/<str:gamecode>/<str:username>', views.TelegramView.as_view(), name='telegram'),
]
