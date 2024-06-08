from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    student = models.ManyToManyField(Student, related_name='course', blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    teacher_name = models.CharField(max_length=100, blank=True, null=True) 
    date_created = models.DateTimeField(auto_now_add=True)
    number = models.CharField(max_length=100, blank=True, null=True)
    academy = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    capacity = models.PositiveIntegerField(blank=True, null=True)
    total_class_hours = models.PositiveIntegerField(choices=[(32, '32 hours'), (48, '48 hours'), (64, '64 hours'), (128, '128 hours')], blank=True, null=True)
    day_of_week = models.CharField(max_length=10, choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/course/{self.id}/"

    def save(self, *args, **kwargs):
        if self.teacher:
            self.teacher_name = self.teacher.name  # 假设 Teacher 模型有一个 name 字段
        super(Course, self).save(*args, **kwargs)