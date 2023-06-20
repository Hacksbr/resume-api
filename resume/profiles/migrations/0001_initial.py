# Generated by Django 4.0.5 on 2023-06-20 02:55

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('skills', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('occupation', models.CharField(max_length=100, verbose_name='Occupation')),
                ('contact_email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='Contact Email')),
                ('phone', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+9999999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Phone')),
                ('city', models.CharField(max_length=100, verbose_name='City')),
                ('country', models.CharField(max_length=80, verbose_name='Country')),
                ('about', models.CharField(blank=True, max_length=550, null=True, verbose_name='About')),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
        migrations.CreateModel(
            name='SocialLink',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('name', models.CharField(choices=[('github', 'GitHub'), ('linkedin', 'LinkedIn'), ('twitter', 'Twitter'), ('website', 'Website'), ('other', 'Other')], max_length=8, verbose_name='Name')),
                ('link', models.CharField(max_length=255, verbose_name='Link')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_links', to='profiles.profile', verbose_name='Profile')),
            ],
            options={
                'verbose_name': 'Social Link',
                'verbose_name_plural': 'Social Links',
            },
        ),
        migrations.CreateModel(
            name='ProfileSkill',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('order', models.PositiveIntegerField(db_index=True, default=0)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_skills', to='profiles.profile', verbose_name='Profile')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_skills', to='skills.skill', verbose_name='Skill')),
            ],
            options={
                'verbose_name': 'Profile Skill',
                'verbose_name_plural': 'Profile Skills',
                'ordering': ['order'],
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='skills',
            field=models.ManyToManyField(blank=True, related_name='profile', through='profiles.ProfileSkill', to='skills.skill'),
        ),
    ]
