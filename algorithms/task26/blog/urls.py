from django.conf.urls.i18n import i18n_patterns
from django.urls import path

from .views import BlogDetailView, AboutPageView, post_list

urlpatterns = [
    path('post/<int:pk>/', BlogDetailView.as_view(), name='post_detail'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('', post_list, name='home')
]
