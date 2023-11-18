from django.shortcuts import render
from django.contrib.auth.models import User
from shivamapp.models import Post
from shivamapp.serializers import PostSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permissions import IsSuperuserOrAuthor
from django.http import JsonResponse

# Create your views here.

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    def get_serializer_context(self):
        return {'is_list_request': True}
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['title', 'body', 'author__username']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'body', 'author__username']
    pagination_class = None
    
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Set the post author to the current user
        serializer.save(author=self.request.user)
        
        # Trigger email notification - Implement this part as needed

class PostRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsSuperuserOrAuthor]

    def perform_update(self, serializer):
        # Ensure the post is updated only by its author
        serializer.save(author=self.request.user)
        # Trigger email notification - Implement this part as needed


class AuthorPostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsSuperuserOrAuthor]
    
    def get_queryset(self):
        author_id = self.kwargs['author_id']
        return Post.objects.filter(author=author_id)

