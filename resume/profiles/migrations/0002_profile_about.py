# Generated by Django 4.0.5 on 2022-11-01 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='about',
            field=models.CharField(blank=True, max_length=550, null=True, verbose_name='About'),
        ),
    ]
