# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.urls import include, path
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from . import views as concept

app_name = "concept"

urlpatterns = [

    path('', concept.BaseView.as_view(), name='home'),
    
    # Login
    path('login/', auth_views.LoginView.as_view(template_name='user/auth.html'), name='login'),

    # Logout
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    #Cadastro de usuario
    path('usuarios/novo/', concept.UserCreateView.as_view(), name='user-create'),

    #Jogo
    path('jogo/home', concept.JogoView.as_view(), name='jogo'),
    path('conceito/novo', concept.ConceptCreateView.as_view(), name='concept-create'),
    path('palavra/nova', concept.WordCreateView.as_view(), name='word-create'),
    path('palavras/', concept.WordView.as_view(), name='words'),
    path('partida/', concept.GameCreateView.as_view(), name='game'),
    path('ranking/palavras', concept.RankingWordsView.as_view(), name='ranking-words'),
    path('ranking/acertos', concept.RankingHitsView.as_view(), name='ranking-hits'),
    path('play/', concept.PlayCreateView.as_view(), name='play-create')
]