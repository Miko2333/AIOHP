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


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    student = models.ManyToManyField(Student, related_name='course',blank=True)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class FileModel(models.Model):
    filename = models.CharField(max_length=50)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')


class Homework(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    file = models.ForeignKey(FileModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Submission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    file = models.ForeignKey(FileModel, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)