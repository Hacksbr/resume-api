# Generated by Django 3.1.2 on 2020-10-31 04:49

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('github', models.CharField(blank=True, max_length=100, null=True, verbose_name='GitHub')),
                ('linkedin', models.CharField(blank=True, max_length=100, null=True, verbose_name='LinkedIn')),
                ('twitter', models.CharField(blank=True, max_length=100, null=True, verbose_name='Twitter')),
                ('website', models.CharField(blank=True, max_length=100, null=True, verbose_name='Website')),
            ],
            options={
                'verbose_name': 'Social Link',
                'verbose_name_plural': 'Social Links',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('occupation', models.CharField(max_length=100, verbose_name='Occupation')),
                ('contact_email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='Contact Email')),
                ('phone', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+9999999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Phone')),
                ('city', models.CharField(max_length=100, verbose_name='City')),
                ('country', models.CharField(max_length=80, verbose_name='Country')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('social_link', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='social_link_profile', to='profiles.sociallink', verbose_name='Social Link ')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
    ]
