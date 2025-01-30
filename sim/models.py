from django.db import models

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=500)


class Message(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    hash = models.TextField( default="default_hash")
    content = models.TextField()
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author}: {self.content or self.file.name}"