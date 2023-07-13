from djongo import models

# Create your models here.

class User(models.Model):
    sno=models.AutoField(primary_key=True)
    username=models.CharField(max_length=300, null=True)
    role=models.CharField(max_length=50, null=True)
    email=models.CharField(max_length=300, null=True)
    password=models.CharField(max_length=300, null=True)


class problems(models.Model):
    sno=models.AutoField(primary_key=True)
    adminEmail=models.CharField(max_length=300, null=True)
    title=models.CharField(max_length=500, null=True)
    question=models.CharField(max_length=100000, null=True)


class testcases(models.Model):
    sno=models.AutoField(primary_key=True)
    adminEmail=models.CharField(max_length=300, null=True)
    questionId=models.IntegerField(max_length=100, null= True)
    input=models.CharField(max_length=10000, null=True)
    output=models.CharField(max_length=500)