import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Users(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'Oddiy foydalanuvchi'),
        ('teacher', 'O\'qituvchi'),
    )
    full_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='F.I.Sh')
    username = models.CharField(max_length=100, null=True, blank=True, verbose_name='Username')
    phone = models.CharField(max_length=100, null=True, blank=True, verbose_name='Telefon raqam')
    telegram_id = models.BigIntegerField(null=True, blank=True, unique=True, verbose_name="Telegram ID")
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default='user', null=True, blank=True,
                            verbose_name='Foydalanuvchi roli')
    joined_at = models.DateTimeField(null=True, blank=True, default=datetime.datetime.now(),
                                     verbose_name="Qo'shilgan vaqti")

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Foydalanuvchilar'
        db_table = 'users'

    def __str__(self):
        return self.full_name


class Student(models.Model):
    first_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Ism")
    last_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Familiya")
    group = models.CharField(max_length=100, null=True, blank=True, verbose_name="Guruhi")
    joined_at = models.DateTimeField(default=datetime.datetime.now(), null=True, blank=True,
                                     verbose_name="Qo'shilgan vaqti")

    class Meta:
        db_table = 'student'
        verbose_name = "Student"
        verbose_name_plural = "O'quvchilar"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class PenaltyBall(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name="Baholangan o'quvchi")
    rated_by = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name="Baholagan shaxs")
    ball = models.IntegerField(validators=[
        MaxValueValidator(10),
        MinValueValidator(1),
    ], null=True, blank=True, verbose_name="Jazo bali")
    created_at = models.DateTimeField(default=datetime.datetime.now(), null=True, blank=True,
                                      verbose_name="Yaratilgan vaqti")

    class Meta:
        db_table = "penalty_ball"
        verbose_name = "Penalty Ball"
        verbose_name_plural = "Jazo ballari"

    def __str__(self):
        return f"{self.student}"
