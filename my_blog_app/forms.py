
from .models import Profile
from django import forms 
from .models import Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class PostForm(forms.ModelForm):
   class Meta:
      model = Post
      fields = ['title', 'category', 'body', 'image']

class CommentForm(forms.ModelForm):
   class Meta:
      model = Comment
      fields = ['content']

class UserRegistrationForm(UserCreationForm):
   email = forms.EmailField() # আমরা চাই ইউজার যেন ইমেইলও দেয়

   class Meta:
      model = User
      fields = ['username', 'email', 'password1', 'password2']
   
class userUpdateFrom(forms.ModelForm):
   email = forms.EmailField()

   class Meta:
      model = User
      fields = ['username', 'email']

class profileUpdateForm(forms.ModelForm):
   
   class Meta:
      model = Profile 
      fields = ['image', 'bio']