from django.contrib import admin
from .views import Post

# Register your models here.
admin.site.register(Post)  # Регистрация модели нашего поста
