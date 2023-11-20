# Generated by Django 4.2.7 on 2023-11-19 10:26

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to=settings.AUTH_USER_MODEL)),
                ('company_id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(help_text='Contact number', max_length=10)),
                ('street', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=50)),
                ('province', models.CharField(max_length=50)),
                ('postal_code', models.CharField(help_text='Postal code', max_length=5)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Expertise',
            fields=[
                ('expertise_id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('skill', models.CharField(help_text="Job seeker's skill", max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='JobFunction',
            fields=[
                ('job_function_id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('function', models.CharField(help_text='Job function description', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='JobSeeker',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to=settings.AUTH_USER_MODEL)),
                ('job_seeker_id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('work_experience', models.DecimalField(decimal_places=1, max_digits=2)),
                ('phone_number', models.CharField(help_text='Contact number', max_length=10)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='JobType',
            fields=[
                ('job_type_id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('type', models.CharField(help_text='Type of job', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Recruiter',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to=settings.AUTH_USER_MODEL)),
                ('recruiter_id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('company_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='careers.company')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='JobOpening',
            fields=[
                ('job_opening_id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('job_title', models.CharField(max_length=30)),
                ('required_work_experience', models.DecimalField(decimal_places=1, max_digits=2)),
                ('min_salary', models.IntegerField()),
                ('max_salary', models.IntegerField()),
                ('job_function', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='careers.jobfunction')),
                ('job_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='careers.jobtype')),
                ('recruiter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='careers.recruiter')),
            ],
        ),
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expertise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='careers.expertise')),
                ('job_opening', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='careers.jobopening')),
            ],
            options={
                'unique_together': {('job_opening', 'expertise')},
            },
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_opening', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='careers.jobopening')),
                ('job_seeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='careers.jobseeker')),
            ],
            options={
                'unique_together': {('job_seeker', 'job_opening')},
            },
        ),
        migrations.CreateModel(
            name='Competence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expertise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='careers.expertise')),
                ('job_seeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='careers.jobseeker')),
            ],
            options={
                'unique_together': {('job_seeker', 'expertise')},
            },
        ),
    ]
