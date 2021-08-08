from django.urls import path
from . import views

app_name = 'dixit'

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('card', views.CardView.as_view(), name='card'),
    path('init/card', views.InitCardView.as_view(), name='initcard'),
    path('rule', views.RuleView.as_view(), name='rule'),
    path('<str:gamecode>/<str:username>', views.GameView.as_view(), name='game'),
    path('login/<str:gamecode>/', views.LoginView.as_view(), name='login'),
    path('telegram/<str:gamecode>/<str:username>', views.TelegramView.as_view(), name='telegram'),
]
