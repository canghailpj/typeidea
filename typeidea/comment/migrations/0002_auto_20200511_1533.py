# Generated by Django 3.0.4 on 2020-05-11 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='target',
            field=models.CharField(max_length=200, verbose_name='评论目标'),
        ),
    ]
