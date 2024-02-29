from django.urls import path

from .views import BlogDetailView, about, post_list, signup_view, login_view, logout_view, \
    neural_network_control_panel_view, neural_network_activation

urlpatterns = [
    path('post/<int:pk>/', BlogDetailView.as_view(), name='post_detail'),
    path('about/', about, name='about'),
    path('', post_list, name='home'),
    path('signup/', signup_view, name='signup_view'),
    path('login/', login_view, name='login_view'),
    path('nn_control_panel/', neural_network_control_panel_view, name='nn_control_panel_view'),
    path('nn_avtivate/', neural_network_activation, name='nn_activate'),
    path('logout/', logout_view, name='logout_view')
]
