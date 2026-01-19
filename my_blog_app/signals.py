
from django.db.models.signals import post_save # সিগন্যালটি পাঠানোর জন্য
from django.contrib.auth.models import User # সিগন্যালটি গ্রহণ করবে User মডেল
from django.dispatch import receiver # এটি হলো রিসিভার
from .models import Profile # প্রোফাইল মডেল যেখানে ডাটা যাবে

# যখনই কোনো নতুন ইউজার তৈরি হবে, এই ফাংশনটি একটি প্রোফাইল তৈরি করবে
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
   if created:
      Profile.objects.create(user=instance)

# ইউজার তথ্য আপডেট করলে প্রোফাইলটিও যেন সেভ হয়
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
   instance.profile.save()