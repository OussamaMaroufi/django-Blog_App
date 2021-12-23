from django.shortcuts import render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin #to check if the user how want to update the postr is  how created it 
from django.contrib.auth.models import User

from .models import Post
from django.views.generic import (ListView,
                                 DetailView,
                                 CreateView,
                                 UpdateView,
                                 DeleteView
                                 )


# Create your views here.

from django.http import HttpResponse

def home(request):

    context = {
        'posts':Post.objects.all()
    }

    return render(request,'blog/home.html',context)



class PostListView(ListView):
    model = Post

    template_name = 'blog/home.html'  
    context_object_name = 'posts'

    ordering = ['-date_posted']
    paginate_by = 4

##################################################
class UserPostListView(ListView):
    model = Post

    template_name = 'blog/user_posts.html'  
    context_object_name = 'posts'

    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))   #get the username from the url 
        return Post.objects.filter(author=user).order_by('-date_posted')



class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        form.instance.author = self.request.user
        self.object.save()
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin ,UpdateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        form.instance.author = self.request.user
        self.object.save()
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:      # prevent user to update any other people post 
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin ,DeleteView):
    model = Post

    success_url='/'


    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:      # prevent user to delete any other people post 
            return True
        return False



def about(request):
    return render(request,'blog/about.html',{'title':'About'})