from django.contrib.auth.models import User
from django.db import models
from  ckeditor.fields import RichTextField

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}'


class Category(models.Model):
    category_name = models.CharField(unique=True,  max_length=255)

    def __str__(self):
        return f'{self.category_name}'



class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    text = RichTextField()
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)