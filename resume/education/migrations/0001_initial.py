# Generated by Django 4.0.5 on 2023-10-05 06:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('school_name', models.CharField(max_length=255, verbose_name='School Name')),
                ('degree', models.CharField(max_length=255, verbose_name='Degree')),
                ('field_of_study', models.CharField(max_length=255, verbose_name='Field of Study')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End Date')),
                ('gpa', models.FloatField(blank=True, default=0.0, null=True, verbose_name='GPA')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('city', models.CharField(max_length=50, verbose_name='City')),
                ('uf', models.CharField(max_length=2, verbose_name='UF')),
                ('country', models.CharField(max_length=50, verbose_name='Country')),
            ],
            options={
                'verbose_name': 'Education',
                'verbose_name_plural': 'Education',
                'ordering': ['-end_date', '-start_date'],
            },
        ),
        migrations.CreateModel(
            name='EducationSkill',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('order', models.PositiveIntegerField(db_index=True, default=0, verbose_name='Order')),
            ],
            options={
                'verbose_name': 'Education Skill',
                'verbose_name_plural': 'Education Skills',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('level', models.CharField(choices=[('basic', 'Elementary proficiency'), ('intermediate', 'Limited working proficiency'), ('advanced', 'Professional working proficiency'), ('fluent', 'Full professional proficiency'), ('native', 'Native or bilingual proficiency')], max_length=12, verbose_name='Level')),
            ],
            options={
                'verbose_name': 'Language',
                'verbose_name_plural': 'Languages',
                'ordering': ['name'],
            },
        ),
    ]
