from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from django.views.generic import DetailView, TemplateView
from .models import Post


def post_list(request):
    all_posts = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(all_posts, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, "home.html", context={'posts': posts})


class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'


class AboutPageView(TemplateView):
    template_name = 'about.html'
