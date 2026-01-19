from django.contrib import admin
from .models import Category, Post, Comment, Profile

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
   list_display = ('title', 'author', 'category', 'created_at')
   prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Profile)

