from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from .filters import PostFilter
from .forms import PostForm, CommentForm
from .models import Post, Author


class PostList(ListView):
    model = Post
    ordering = 'time_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

def post_create(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = Author.objects.get(user=request.user)
            form.save()
            return HttpResponseRedirect('/')

    return render(request, 'post_edit.html', {'form': form})


class PostDetail(LoginRequiredMixin, DetailView):
    form_class = CommentForm
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.object.category.all()
        context['author'] = self.object.author
        return context


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = 'news_portal.update_post'

    def get_success_url(self):
        return reverse_lazy('post', kwargs={'pk': self.object.pk})

class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    permission_required = 'news_portal.delete_post'

    def get_success_url(self):
        return reverse_lazy('post_list')
@login_required
def become_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        Author.objects.create(user=user)
    return redirect('/')