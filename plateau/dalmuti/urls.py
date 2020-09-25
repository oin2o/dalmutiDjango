from django.urls import path

from . import views

app_name = 'dalmuti'

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('<str:username>', views.MainView.as_view(), name='main'),
    path('rule/<str:username>', views.RuleView.as_view(), name='rule'),
    path('newgame/<str:username>', views.NewGameView.as_view(), name='newgame'),
    path('<str:gamename>/<str:username>', views.InGameView.as_view(), name='ingame'),
    path('pick/<str:gamename>/<str:username>/<str:card>', views.PickView.as_view(), name='pick'),
    path('shuffle/<str:gamename>/<str:username>', views.ShuffleView.as_view(), name='shuffle'),
    path('cardok/<str:gamename>/<str:username>', views.CardOKView.as_view(), name='cardok'),
    path('revolution/<str:gamename>/<str:username>', views.RevolutionView.as_view(), name='revolution'),
    path('gameend/<str:gamename>/<str:username>', views.GameEndView.as_view(), name='gameend'),
    path('gamequit/<str:gamename>/<str:username>', views.GameQuitView.as_view(), name='gamequit'),
]
