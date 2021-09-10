from django.db import models
from django.contrib.auth.models import User


class StudentUser(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10,null=True)
    image = models.FileField(null=True)
    gender = models.CharField(max_length=10,null=True)
    type = models.CharField(max_length=10,null=True)
    resume = models.FileField(null=True)

    def __str__(self):
        return self.user.username


class Recruiter(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10,null=True)
    image = models.FileField(null=True)
    gender = models.CharField(max_length=10,null=True)
    company = models.CharField(max_length=50,null=True)
    status = models.CharField(max_length=20,null=True)
    type = models.CharField(max_length=10,null=True)

    def __str__(self):
        return self.user.username

class Job(models.Model):
    recruiter = models.ForeignKey(Recruiter,on_delete=models.CASCADE,null=True,blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    salary = models.CharField(max_length=10,null=True)
    permonth = models.CharField(max_length=10)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    experience = models.CharField(max_length=10)
    location = models.CharField(max_length=15)
    skill = models.CharField(max_length=300,null=True)
    creationdate = models.DateField()
    company = models.CharField(max_length=50)
    paid = models.CharField(max_length=10,null=True,blank=True)

    def __str__(self):
        return self.title







class Apply(models.Model):
    job = models.ForeignKey(Job,on_delete=models.CASCADE,null=True)
    student= models.ForeignKey(StudentUser,on_delete=models.CASCADE,null=True)
    resume = models.FileField(null=True)
    applied_date = models.DateField(null=True)
    status = models.CharField(max_length=300,null=True,blank=True)
    interviewdateaandtime = models.DateTimeField(null=True,blank=True)
    joiningletter = models.FileField(null=True, blank=True)

    def __str__(self):
        return str(self.id)




class Video(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    caption = models.CharField(null=True,max_length=100)
    video=models.FileField(null=True)
    thumbnail=models.FileField(null=True)
    type=models.CharField(null=True,max_length=100)
    creationdate = models.DateField(null=True)

    def __str__(self):
        return self.caption


class Feedback(models.Model):
    title = models.CharField(max_length=30,null=True)
    content = models.CharField(max_length=100,null=True)
    date = models.DateField(max_length=100,null=True)

    def __str__(self):
        return self.title

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)