from django.urls import path

from shivamapp.views import PostListCreateView,PostRetrieveUpdateDeleteView,AuthorPostListView

urlpatterns = [
    path('api/posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('api/posts/<int:pk>/', PostRetrieveUpdateDeleteView.as_view(), name='post-retrieve-update-delete'),
    path('api/posts/filter/author/<int:author_id>/', AuthorPostListView.as_view(), name='author-post-list'),
   
]