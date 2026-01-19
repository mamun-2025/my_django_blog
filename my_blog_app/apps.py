from django.apps import AppConfig


class MyBlogAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_blog_app' # নিশ্চিত হোন এখানে আপনার সঠিক অ্যাপের নাম আছে

    # সিগন্যাল কানেক্ট করার জন্য এই মেথডটি যোগ করতে হবে
    def ready(self):
        import my_blog_app.signals

