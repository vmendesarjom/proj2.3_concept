# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import uuid

from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import AbstractUser, Group, Permission

from django.db import models

# CreateUpdateModel
# - - - - - - - - - - - - - - - - - - -
class CreateUpdateModel(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em', auto_now=True)

    class Meta:
        abstract = True

# UUIDUser
# - - - - - - - - - - - - - - - - - - -
class UUIDUser(AbstractUser):

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	groups = models.ManyToManyField(Group, blank=True, related_name="uuiduser_set", related_query_name="user")
	user_permissions = models.ManyToManyField(Permission, blank=True, related_name="uuiduser_set", related_query_name="user")
	pontos_hit = models.IntegerField(default=0)
	pontos_word = models.IntegerField(default=0)

	def __str__(self):
		return self.username

	class Meta:
		verbose_name = 'usuário'
		verbose_name_plural = 'usuários'

#Conceito
#--------------------------------------
class Conceito (models.Model):

	concept = models.CharField(max_length=255, null=False, unique=True, blank=False, verbose_name='conceito')

	def __str__(self):
		return self.concept

	class Meta:
		verbose_name = 'Conceito'
		verbose_name_plural = 'Conceitos'

#Palavra
#--------------------------------------
class Palavra (models.Model):

	word = models.CharField(max_length=255, null=False, blank=False, verbose_name='palavra')
	concepts = models.ManyToManyField(Conceito, blank=False, related_name='conceitos', verbose_name='conceito')
	user = models.ForeignKey(UUIDUser, on_delete=models.CASCADE, related_name='usuarios', verbose_name='usuario')

	def __str__(self):
		return self.word

	class Meta:
		verbose_name = 'Palavra'
		verbose_name_plural = 'Palavras'

#Partida
#--------------------------------------
class Partida (models.Model):

	user = models.ForeignKey(UUIDUser, on_delete=models.CASCADE, related_name='partida', verbose_name='usuario')
	word = models.ForeignKey(Palavra, on_delete=models.CASCADE, related_name='partida', verbose_name='palavra')

	def __str__(self):
		return self.word.word

	class Meta:
		verbose_name = 'Partida'
		verbose_name_plural = 'Partidas'