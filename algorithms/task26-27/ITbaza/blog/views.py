from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout

from django.views.generic import DetailView, TemplateView
from .models import Post
from .forms import SignUpForm, LoginForm


def post_list(request):
    current_user = request.user
    all_posts = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(all_posts, 3)
    page = request.GET.get('page')
    if page is None:
        page = '1'
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    is_logged = current_user.is_authenticated
    return render(request, "home.html", context={'posts': posts, 'user': current_user, 'is_logged': is_logged, 'page': page})


class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'


def about(request):
    current_user = request.user
    is_logged = current_user.is_authenticated
    return render(request, 'about.html', context={'user': current_user, 'is_logged': is_logged})


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'error.html', {'form': form}) # Probably a failsave, should be repaced with a proper error page


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'error.html', {'form': form}) # Probably a failsafe, should be replaced with a proper error page


def logout_view(request):
    logout(request)
    return redirect('home')

def neural_network_control_panel_view(request):
    is_superuser = request.user.is_superuser
    if is_superuser:
        return render(request, 'nn_control_panel.html')
    else:
        return render(request, 'error.html', {'text': 'You do not have permissions to access this page!'})

def neural_network_activation(request):
    post_data = request.POST
    nn_type = post_data['nn_type']
    start_time = post_data['start_time']
    prediction_time = post_data['prediction_time']
    to_do = post_data['todo']

    # some logic

