# Generated by Django 2.0.7 on 2018-09-24 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sucesso', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='uuiduser',
            name='pontos_hit',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='uuiduser',
            name='pontos_word',
            field=models.IntegerField(default=0),
        ),
    ]
