from django.contrib import admin

from .models import *

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'username', 'role', 'joined_at')
    list_filter = ('joined_at', 'role')
    search_fields = ('full_name', 'username', 'role')
    date_hierarchy = 'joined_at'

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'group', 'joined_at')
    list_filter = ('joined_at', 'group')
    search_fields = ('first_name', 'last_name', 'group')
    date_hierarchy = 'joined_at'

@admin.register(PenaltyBall)
class PenaltyBallAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'rated_by', 'ball', 'created_at')
    list_filter = ('created_at', 'rated_by')
    search_fields = ('student__first_name', 'student__last_name', 'rated_by__full_name', 'ball')
    date_hierarchy = 'created_at'