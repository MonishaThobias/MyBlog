from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateField(default=timezone.now)
    created_time = models.TimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

 
    def __str__(self):
        return f"{self.title} ({self.created_date})"  # This returns a string


    class Meta:
        ordering = ['-created_date', '-created_time']  # Newest posts first

class Subscriber(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "Subscribers"

