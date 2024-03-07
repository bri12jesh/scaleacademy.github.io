from django.db import models
import uuid

# Create your models here.

class register(models.Model):
    id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=254)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=1000)
    mobile=models.CharField(max_length=255)
    

class payment(models.Model):
    id=models.AutoField(primary_key=True)
    # user=models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    course_instructor=models.CharField(max_length=255)
    course_name=models.CharField(max_length=255)
    course_amount = models.CharField(max_length=50)
    dateofpurchase=models.DateField()
    dateofexpiry=models.DateField()

class courseInfo(models.Model):
    id=models.AutoField(primary_key=True)
    course_Img=models.URLField(max_length=2000)
    course_duration=models.CharField(max_length=255)
    course_instructor=models.CharField(max_length=255)
    course_name=models.CharField(max_length=255)
    course_amount = models.CharField(max_length=50)

class userdetails(models.Model):
    id=models.AutoField(primary_key=True)
    firstname=models.CharField(max_length=254)
    lastname=models.CharField(max_length=254)
    email=models.CharField(max_length=255)
    gender=models.CharField(max_length=1000)
    mobile=models.CharField(max_length=255)
    profession=models.CharField(max_length=255)
    img=models.URLField(max_length=255)
    

# class tokenUser(models.Model):
#     email=models.CharField(max_length=255)
#     token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
