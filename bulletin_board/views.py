from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import ModelFormMixin, FormMixin

from .filters import PostFilter
from .forms import PostForm, CommentForm
from .models import Post, Author, Comment


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


class PostDetail(LoginRequiredMixin, FormMixin, DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    form_class = CommentForm

    def get_success_url(self):
        return reverse_lazy('post', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context['post']
        user = self.request.user
        context['category'] = self.object.category.all()
        context['form'] = self.get_form()
        context['author'] = self.object.author
        context['form'] = self.get_form()
        # context['comments'] = self.object.comments.all()
        comments = Comment.objects.filter(post=post)

        accepted_comments = comments.filter(accept=True)
        unaccepted_comments = comments.filter(accept=False)
        context['accepted_comments'] = accepted_comments
        context['unaccepted_comments'] = unaccepted_comments
        if user.is_authenticated:
            user_comments = comments.filter(created_by=user)
            context['user_comments'] = user_comments


        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        print(comment.post)
        comment.author = self.object.author
        comment.created_by = self.request.user
        comment.save()

        return super().form_valid(form)



class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = 'bulletin_board.update_post'

    def get_success_url(self):
        return reverse_lazy('post', kwargs={'pk': self.object.pk})

class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    permission_required = 'bulletin_board.delete_post'

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


class UserPostsAndCommentsView(LoginRequiredMixin, ListView):
    template_name = 'user_posts_and_comments.html'
    context_object_name = 'posts'

    def get_queryset(self, **kwargs):
        user_id = self.request.user.id
        author = Author.objects.get(user_id=user_id)
        author_id = author.id  # Получаем id пользователя
        print(author_id)
        posts = Post.objects.filter(author_id=author_id)
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = context['posts']
        # Не нужно добавлять комментарии вручную, Django автоматически предоставит их через related_name
        context['posts'] = posts
        return context


class CommentDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Comment
    template_name = 'comment_delete.html'
    permission_required = 'bulletin_board.delete_comment'

    def get_success_url(self):
        return reverse_lazy('user_posts_and_comments')

@login_required
def accept_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        comment.accept = True
        comment.save()
    return redirect('user_posts_and_comments')