# Generated by Django 5.0.4 on 2024-05-02 06:42

import django.contrib.auth.models
import django.contrib.auth.validators
import django.utils.timezone
import django_countries.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('full_name', models.CharField(blank=True, max_length=50, verbose_name='full_name')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='path/to/upload/', verbose_name='profile picture')),
                ('bio', models.TextField(blank=True, max_length=500, verbose_name='Bio')),
                ('source', models.CharField(blank=True, max_length=75, verbose_name='source')),
                ('contact', models.CharField(blank=True, max_length=50, null=True, verbose_name='contact')),
                ('age', models.PositiveIntegerField(default=18)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('Passport_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='Official ID')),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female')], default='male', max_length=20, verbose_name='Gender')),
                ('nationality', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'indexes': [models.Index(fields=['email', 'username', 'bio', 'source', 'contact', 'full_name', 'country', 'gender', 'nationality'], name='users_custo_email_4079f2_idx')],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
