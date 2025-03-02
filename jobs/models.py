from django.db import models
from cloudinary.models import CloudinaryField

class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    description = models.TextField()
    skills = models.CharField(max_length=255)
    image = CloudinaryField('image')
    apply_link = models.URLField()
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title