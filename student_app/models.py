from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
import random
import string

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    dob = models.DateField()
    place = models.CharField(max_length=100)
    college_name = models.CharField(max_length=200)
    blood_group = models.CharField(max_length=5)
    image = models.ImageField(upload_to='student_images/')

    def __str__(self):
        return self.full_name