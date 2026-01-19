
import os
from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

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
   image = models.ImageField(null=True, blank=True, upload_to='blog_images/')
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
   image = models.ImageField(default='default.jpg', upload_to='profile_pics')
   bio = models.TextField(blank=True)

   def __str__(self):
      return f"{self.user.username} Profile"

   def save(self, *args, **kwargs):
      super().save(*args, **kwargs) # প্রথমে ছবিটিকে সেভ করে নেবে

      # শুধু তখনই ইমেজ ওপেন করবে যদি ফাইলটি হার্ডড্রাইভে থাকে
      if self.image and os.path.exists(self.image.path):
         img = Image.open(self.image.path) # ছবির লোকেশন খুঁজে ওপেন করবে

         # যদি ছবি ৩০০ পিক্সেলের চেয়ে বড় হয়, তবে তাকে ছোট করবে
         if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path) # একই জায়গায় ছোট ছবিটিকে রিপ্লেস করবে

   
      