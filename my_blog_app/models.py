
import os
from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from cloudinary.models import CloudinaryField

class Category(models.Model):
   name = models.CharField(max_length=100)
   slug = models.SlugField(unique=True, blank=True)
   
   class Meta:
        verbose_name_plural = "Categories"

   def save(self, *args, **Kwargs):
      if not self.slug:
         self.slug = slugify(self.name)
      super().save(*args, **Kwargs)

   def __str__(self):
      return self.name
   
class Post(models.Model):
   title = models.CharField(max_length=200)
   slug = models.SlugField(unique=True, blank=True)
   author = models.ForeignKey(User, on_delete=models.CASCADE)
   category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
   body = models.TextField()
   image = CloudinaryField('image', null=True, blank=True)
   created_at = models.DateTimeField(auto_now_add=True)

   def save(self, *args, **kwargs):
      if not self.slug:
         self.slug = slugify(self.title)
      super().save(*args, **kwargs)
   
   def __str__(self):
      return self.title

class Comment(models.Model):
   post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   content = models.TextField()
   date_added = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   image = CloudinaryField('image', default='default.jpg')
   bio = models.TextField(blank=True)

   def __str__(self):
      return f"{self.user.username} Profile"

   def save(self, *args, **kwargs):
      super().save(*args, **kwargs) 
