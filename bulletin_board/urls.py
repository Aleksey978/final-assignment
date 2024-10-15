from django.urls import path
from .views import PostList, post_create, PostDetail, PostUpdate, PostDelete, become_author, UserPostsAndCommentsView, \
   CommentDelete, accept_comment

urlpatterns = [
   path('', PostList.as_view(), name='post_list'),
   path('<int:pk>',PostDetail.as_view(), name='post'),
   path('create/', post_create, name='post_create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('become_author/', become_author, name='become_author'),
   path('my-posts/', UserPostsAndCommentsView.as_view(), name='user_posts_and_comments'),
   path('<int:pk>/comment_delete/', CommentDelete.as_view(), name='comment_delete'),
   path('accept-comment/<int:comment_id>/', accept_comment, name='accept_comment'),
]
