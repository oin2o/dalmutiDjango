from django.urls import path

from . import views

app_name = 'dalmutip'

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('<str:username>', views.MainView.as_view(), name='main'),
    path('rule/<str:username>', views.RuleView.as_view(), name='rule'),
    path('honor/<str:username>', views.HonorView.as_view(), name='honor'),
    path('ranking/<str:username>', views.RankView.as_view(), name='rank'),
    path('newgame/<str:username>', views.NewGameView.as_view(), name='newgame'),
    path('<str:gamename>/<str:username>', views.InGameView.as_view(), name='ingame'),
    path('game/<str:gamename>/<str:username>', views.PrivateGameView.as_view(), name='private'),
    path('pick/<str:gamename>/<str:username>/<str:card>', views.PickView.as_view(), name='pick'),
    path('shuffle/<str:gamename>/<str:username>', views.ShuffleView.as_view(), name='shuffle'),
    path('cardok/<str:gamename>/<str:username>', views.CardOKView.as_view(), name='cardok'),
    path('revolution/<str:gamename>/<str:username>', views.RevolutionView.as_view(), name='revolution'),
    path('gameend/<str:gamename>/<str:username>', views.GameEndView.as_view(), name='gameend'),
    path('gamequit/<str:gamename>/<str:username>', views.GameQuitView.as_view(), name='gamequit'),
    path('cardallin/<str:gamename>/<str:username>', views.CardAllInView.as_view(), name='cardallin'),
    path('autopass/<str:gamename>/<str:username>', views.AutoPassView.as_view(), name='autopass'),
    path('roundrenew/<str:gamename>/<str:username>', views.RoundRenewView.as_view(), name='roundrenew'),
    path('intrusion/<str:gamename>/<str:username>', views.IntrusionView.as_view(), name='intrusion'),
    path('imgchange/<str:gamename>/<str:username>', views.ImageChangeView.as_view(), name='imgchange'),
]
