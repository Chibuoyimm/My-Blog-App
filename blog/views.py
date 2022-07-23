from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post


posts = [
    {
        'author': 'Chibuoyim',
        'title': 'Blog Post1',
        'content': 'First Post Content',
        'date_posted': 'September 17, 2021'
    },
    {
        'author': 'Olumide',
        'title': 'Blog Post2',
        'content': 'Second Post Content',
        'date_posted': 'September 18, 2021'
    }
]


def home(request):
    context = {'posts': Post.objects.all()}
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html  (convention of template it looks for by default)
    context_object_name = 'posts' # 'object_list' is the default context name it looks for
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # <app>/<model>_<viewtype>.html  (convention of template it looks for by default)
    context_object_name = 'posts' # 'object_list' is the default context name it looks for
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author






def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
# Create your views here.
