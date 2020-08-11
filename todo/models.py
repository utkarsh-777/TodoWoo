from django.db import models
from django.contrib.auth.models import User

class TodoModel(models.Model):
    Title = models.CharField(max_length = 150)
    Description = models.TextField(blank=True)
    Date = models.DateTimeField(auto_now_add=True)
    DateCompleted = models.DateTimeField(null=True,blank=True)
    Important = models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.Title