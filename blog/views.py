from django.shortcuts import render, get_object_or_404
from .models import Post, User
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.

dummy_posts = [
    {
        'author_name': 'Mrugank Ray',
        'title': 'article one',
        'content': 'content 1',
        'published_date': 'april, 27 2020'
    },
    {
        'author_name': 'Mayank Ray',
        'title': 'article two',
        'content': 'content 2',
        'published_date': 'april, 28 2020'
    }
]


def home(req):
    context = {
        'posts': Post.objects.all()
    }
    return render(req, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 3


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author_name=user).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create_post.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author_name = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/create_post.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author_name = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if post.author_name == self.request.user:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    fields = ['title', 'content']
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if post.author_name == self.request.user:
            return True
        return False


def about(req):
    return render(req, 'blog/about.html', {'title': 'About'})
