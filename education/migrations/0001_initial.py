# Generated by Django 5.1.2 on 2024-10-24 07:54

import datetime
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Ism')),
                ('last_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Familiya')),
                ('group', models.CharField(blank=True, max_length=100, null=True, verbose_name='Guruhi')),
                ('joined_at', models.DateTimeField(blank=True, default=datetime.datetime(2024, 10, 24, 12, 54, 57, 782118), null=True, verbose_name="Qo'shilgan vaqti")),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': "O'quvchilar",
                'db_table': 'student',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='F.I.Sh')),
                ('username', models.CharField(blank=True, max_length=100, null=True, verbose_name='Username')),
                ('phone', models.CharField(blank=True, max_length=100, null=True, verbose_name='Telefon raqam')),
                ('telegram_id', models.BigIntegerField(blank=True, null=True, unique=True, verbose_name='Telegram ID')),
                ('role', models.CharField(blank=True, choices=[('admin', 'Admin'), ('user', 'Oddiy foydalanuvchi'), ('teacher', "O'qituvchi")], default='user', max_length=100, null=True, verbose_name='Foydalanuvchi roli')),
                ('joined_at', models.DateTimeField(blank=True, default=datetime.datetime(2024, 10, 24, 12, 54, 57, 782118), null=True, verbose_name="Qo'shilgan vaqti")),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Foydalanuvchilar',
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='PenaltyBall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ball', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)], verbose_name='Jazo bali')),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime(2024, 10, 24, 12, 54, 57, 782118), null=True, verbose_name='Yaratilgan vaqti')),
                ('penalty_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='education.student', verbose_name="Baholangan o'quvchi")),
                ('rated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='education.users', verbose_name='Baholagan shaxs')),
            ],
            options={
                'verbose_name': 'Penalty Ball',
                'verbose_name_plural': 'Jazo ballari',
                'db_table': 'penalty_ball',
            },
        ),
    ]
