
from django.shortcuts import  render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, CommentForm

from django.views.generic import (
   ListView,
   DetailView,
   CreateView, 
   UpdateView, 
   DeleteView
   )
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from .forms import userUpdateFrom, profileUpdateForm



class PostListView(ListView):
   model = Post
   template_name = 'my_blog_app/home.html'
   context_object_name = 'posts'
   ordering = ['-created_at']

class PostDetailView(DetailView):
   model = Post
   template_name = 'my_blog_app/post_detail.html'
   context_object_name = 'post'

   # টেমপ্লেটে ফর্মটি পাঠানোর জন্য এই মেথডটি যোগ করুন
   def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          context["form"] = CommentForm()
          return context
   
   # কমেন্ট সেভ করার জন্য এই মেথডটি যোগ করুন
   def post(self, request, *args, **kwargs):
       post = self.get_object()
       form = CommentForm(request.POST)
       if form.is_valid():
           comment = form.save(commit=False)
           comment.post = post
           comment.user = request.user
           comment.save()
           return redirect('post-detail', slug=post.slug)
       return self.get(request, *args, **kwargs)

# ৩. এখন নতুন ৩টি ক্লাস (Create, Update, Delete) নিচে যোগ করে দিন
# নতুন পোস্ট তৈরি করার জন্য
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'category', 'body', 'image']
    template_name = 'my_blog_app/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user # বর্তমানে লগইন থাকা ইউজারকে লেখক হিসেবে সেট করবে
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'slug': self.object.slug})
    
# পোস্ট এডিট করার জন্য
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'category', 'body', 'image']
    template_name = 'my_blog_app/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author # শুধু লেখকই এডিট করতে পারবে

# পোস্ট ডিলিট করার জন্য
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'my_blog_app/post_confirm_delete.html'
    success_url = '/' # ডিলিট হওয়ার পর হোম পেজে যাবে

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
# --- ইউজার রেজিস্ট্রেশন ভিউ (Function Based View) ---
def register(request):
    # যদি ইউজার ফর্ম সাবমিট করে (POST রিকোয়েস্ট)
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save() # ডাটাবেজে ইউজার তৈরি হবে
            username = form.cleaned_data.get('username')
            # সাকসেস মেসেজ পাঠানো
            messages.success(request, f"Account created for {username}! you can now login.")
            return redirect('login') # ইউজারকে লগইন পেজে পাঠিয়ে দেওয়া
    else:
            # যদি ইউজার প্রথমবার পেজে আসে (GET রিকোয়েস্ট)
            form = UserRegistrationForm()
    return render(request, 'my_blog_app/register.html', {'form': form})

# @login_required ডেকোরেটর ব্যবহার করব, যাতে কেউ লগইন না করে প্রোফাইল পেজে ঢুকতে না পারে।
@login_required
def profile(request):
    if request.method == 'POST':
    # এখানে 'userUpdateFrom' এবং 'profileUpdateForm' আপনার forms.py এর বানানের সাথে মিল রেখে লেখা হয়েছে
        u_form = userUpdateFrom(request.POST, instance=request.user)
        p_form = profileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Your account has been updated!")
            return redirect('profile')  # আপডেট হওয়ার পর আবার প্রোফাইল পেজেই নিয়ে যাবে
    else:
            u_form = userUpdateFrom(instance=request.user)
            p_form = profileUpdateForm(instance=request.user.profile) 

    context = {
        'u_form': u_form,
        'p_form': p_form
    }  
    return render(request, 'my_blog_app/profile.html', context)


def about(request):
    return render(request, 'my_blog_app/about.html')