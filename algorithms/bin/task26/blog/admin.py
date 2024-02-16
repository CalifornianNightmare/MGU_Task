from django.contrib import admin
from .views import Post

# This somehow makes post creation on admin panel
admin.site.register(Post)
