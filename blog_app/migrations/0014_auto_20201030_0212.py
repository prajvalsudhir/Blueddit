# Generated by Django 3.0.2 on 2020-10-29 20:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog_app', '0013_auto_20201030_0042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='user_like', to=settings.AUTH_USER_MODEL),
        ),
    ]
