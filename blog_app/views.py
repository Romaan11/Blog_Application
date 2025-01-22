from django.shortcuts import render
from blog_app.models import Post
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from blog_app.forms import PostForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.

from django.views.generic import ListView, DetailView, CreateView, UpdateView, View

class PostListView(ListView):
    model = Post
    template_name = "post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        posts = Post.objects.filter(published_at__isnull = False).order_by(
            "published_at"
        )
        return posts
    


class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        queryset = Post.objects.filter(pk=self.kwargs["pk"], published_at__isnull = False)
        return queryset


class DraftListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "draft_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        queryset = Post.objects.filter(published_at__isnull=True)
        return queryset
    

class DraftDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "draft_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        queryset = Post.objects.filter(pk = self.kwargs["pk"], published_at__isnull = True)
        return queryset




class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect("post-list")


class PostPublishView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk, published_at__isnull = True)
        post.published_at = timezone.now()
        post.save()
        return redirect("post-list")


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "post_create.html"
    form_class = PostForm
    # success_url = reverse_lazy("post-list") # This will lead us to post-list when we have successfully created a post

    # To go to draft-detail instead of post-list we have to do the following code
    def get_success_url(self):
        return reverse_lazy("draft-detail", kwargs={"pk":self.object.pk})
    # Now after the code is created successfully we will be sent to draft-detail


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

# @login_required
# def post_create(request):
#     form = PostForm()
#     if request.method == "POST":
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             return redirect("draft-detail", pk=post.pk)
        
#     return render(
#         request,
#         "post_create.html",
#         {"form": form},
#     )


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "Post_create.html"
    form_class = PostForm

    def get_success_url(self):
        post = self.get_object()
        if post.published_at:
            return reverse_lazy("post-detail", kwargs={"pk": post.pk})
        else:
            return reverse_lazy("draft-detail", kwargs={"pk": post.pk})




# CRUD => Create, Read, Update, Delete
# function based views
# class based views