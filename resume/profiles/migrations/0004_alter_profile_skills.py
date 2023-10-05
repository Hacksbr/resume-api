# Generated by Django 4.0.5 on 2023-10-04 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0001_initial'),
        ('profiles', '0003_alter_profile_skills'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='skills',
            field=models.ManyToManyField(blank=True, related_name='profile', through='profiles.ProfileSkill', to='skills.skill'),
        ),
    ]
