# -*- coding: utf-8 -*-

from django.shortcuts import render

from . import models
from .forms import UUIDUserForm

from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy, reverse

from django.http import HttpResponseRedirect

# Base Template View
#----------------------
class BaseView(TemplateView):

    template_name = 'casa.html'

# Jogo Template View
#----------------------
class JogoView(TemplateView):

    template_name = 'jogo/jogo.html'

# User Create View
#----------------------
class UserCreateView(CreateView):
    
    model = models.UUIDUser
    template_name = 'user/form.html'
    success_url = reverse_lazy('concept:login')
    form_class = UUIDUserForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.set_password(obj.password)
        obj.save()
        return super(UserCreateView, self).form_valid(form)

# Concept Create View
#----------------------
class ConceptCreateView(CreateView):

    model = models.Conceito
    template_name = 'jogo/cad_conceito.html'
    success_url = reverse_lazy('concept:jogo')
    fields = ['concept']

# Word Create View
#----------------------
class WordCreateView(CreateView):

    model = models.Palavra
    template_name = 'jogo/cad_palavra.html'
    success_url = reverse_lazy('concept:jogo')
    fields = ['word', 'concepts']

    def post(self, request, *args, **kwargs):
        conc = dict(self.request.POST)
        p = models.Palavra.objects.create(user=self.request.user)
        for c in conc["concepts"]:
            p.concepts.add(c)
        p.word = self.request.POST.get("word")
        p.save()
                
        return HttpResponseRedirect(reverse('concept:jogo'))

# Word List View
#-----------------------
class WordView(ListView):

    model = models.Palavra
    template_name = 'jogo/palavra.html'

    def get_context_data(self, **kwargs):
        object_list = []
        if self.request.user.is_staff:
            for x in models.Palavra.objects.all():
                object_list.append(x)
            kwargs['object_list'] = object_list
        else:
            for x in models.Palavra.objects.filter(user = self.request.user):
                object_list.append(x)
            kwargs['object_list'] = object_list
        return super(WordView, self).get_context_data(**kwargs)

# Game Create View
#----------------------
class GameCreateView(CreateView):

    model = models.Partida
    template_name = 'jogo/partida.html'
    fields = ["user", "word"]
    sucess_url = reverse_lazy("concept:jogo")

    def post(self, request, *args, **kwargs):
        pal = models.Palavra.objects.first()
        cont = 0
        for palavra in models.Palavra.objects.exclude(user=self.request.user):
            for partida in models.Partida.objects.filter(user=self.request.user):
                if palavra == partida.word:
                    cont += 1
                else:
                    pal = palavra
        if cont == 0:
            word = pal
        else:
            word = pal                
        try:
            obj = models.Partida.objects.create(user = self.request.user, word = word)
            obj.save()
        
            return HttpResponseRedirect(reverse('concept:play-create'))
        except Exception as e:
            print(e.message())
            return HttpResponseRedirect(reverse('concept:jogo'))

class PlayCreateView(CreateView):
    
    model = models.Partida
    template_name = 'jogo/play.html'
    fields = ["word"]
    sucess_url = reverse_lazy("concept:jogo")

    def post(self, request, *args, **kwargs):
        for partida in models.Partida.objects.filter(user=self.request.user).order_by('-id'):
            while True:    
                if partida.word == self.request.POST.get('nome'):
                    partida.user.pontos_hit += 2
                    partida.word.user.pontos_word += 1
                    return HttpResponseRedirect(reverse('concept:home'))
                else:
                    return HttpResponseRedirect(reverse('concept:play-create'))
    
    def get_context_data(self, **kwargs):
        object_list = models.Partida.objects.filter(user=self.request.user).order_by('-id')
        kwargs['object_list'] = object_list
        return super(PlayCreateView, self).get_context_data(**kwargs)


# Ranking Hits View
#----------------------
class RankingHitsView(ListView):
    
    model = models.UUIDUser
    template_name = 'jogo/ranking_acertos.html'
    
    def get_context_data(self, **kwargs):
        object_list = models.UUIDUser.objects.all().order_by('pontos_hit')
        kwargs['object_list'] = object_list
        return super(RankingHitsView, self).get_context_data(**kwargs)

# Ranking Words View
#----------------------
class RankingWordsView(ListView):

    model = models.UUIDUser
    template_name = 'jogo/ranking_palavras.html'

    def get_context_data(self, **kwargs):
        object_list = models.UUIDUser.objects.all().order_by('pontos_word')
        kwargs['object_list'] = object_list
        return super(RankingWordsView, self).get_context_data(**kwargs)