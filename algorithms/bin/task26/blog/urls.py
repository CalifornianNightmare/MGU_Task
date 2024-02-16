from django.conf.urls.i18n import i18n_patterns
from django.urls import path

from .views import BlogDetailView, AboutPageView, post_list, signup_view, login_view, logout_view

urlpatterns = [
    path('post/<int:pk>/', BlogDetailView.as_view(), name='post_detail'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('', post_list, name='home'),
    path('signup/', signup_view, name='signup_view'),
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view')
]
