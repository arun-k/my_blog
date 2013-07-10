from django.db import models

# Create your models here.
class Blog(models.Model):
    #blog_id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=30)
    topic=models.TextField()
    content=models.TextField()
    created=models.DateField()

class Comment(models.Model):
    postId=models.IntegerField()
    name=models.CharField(max_length=50)
    body=models.TextField()
    date=models.DateTimeField(auto_now_add=True)
