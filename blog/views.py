from django.shortcuts import render, get_object_or_404
from django.views.generic import (ListView, 
                                DetailView,
                                CreateView,
                                UpdateView,
                                DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Post

'''
posts = [
    {
        'author':'Peeyush Kumar',
        'title':'My Blog Post',
        'content':'This is the content of my first blog post',
        'dateposted':'May 2,2020'
    },
    {
        'author':'Aroosh Kumar',
        'title':'His Blog Post',
        'content': 'This is the content of Aroosh\'s first blog post',
        'dateposted':'May 1, 2020'
    }
]
'''
# Create your views here.
def home(request):
    context = {
        'posts':Post.objects.all()
    }
    return render(request, 'blog/home.html',context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' #<app>/<model>_<viewtype>.html'
    context_object_name ='posts'
    order = ['-date-posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' #<app>/<model>_<viewtype>.html'
    context_object_name ='posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author = user).order_by('date_posted')

class PostDetailView(DetailView):
    model = Post
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
       
    def test_func(self):
        Post = self.get_object()
        if self.request.user == Post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Post
    success_url ='/'

    def test_func(self):
        Post = self.get_object()
        if self.request.user == Post.author:
            return True
        return False

       
def about(request):
     return render(request, 'blog/about.html',{'title':'About'})

