
from django.urls import path
from .views import (
   PostListView,
   PostDetailView,
   PostCreateView,
   PostUpdateView,
   PostDeleteView
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post-detail'), 
    path('post/<slug:slug>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<slug:slug>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
]
