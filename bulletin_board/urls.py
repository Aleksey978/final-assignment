from django.urls import path
from .views import PostList, post_create, PostDetail, PostUpdate, PostDelete, become_author


urlpatterns = [
   path('', PostList.as_view(), name='post_list'),
   path('<int:pk>',PostDetail.as_view(), name='post'),
   path('create/', post_create, name='post_create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('become_author/', become_author, name='become_author'),
]