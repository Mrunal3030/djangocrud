from django.shortcuts import render
from django.contrib.auth.models import User
from shivamapp.models import Post
from shivamapp.serializers import PostSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import authentication_classes, permission_classes
# authnetication
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permissions import IsSuperuserOrAuthor
from django.http import JsonResponse





class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Call the parent class to perform the default JWT authentication
        result = super().authenticate(request)

        # Check if the result is not None
        if result is not None:
            user, validated_token = result
            # Check if the user is authenticated
            if user and user.is_authenticated:
                return user, validated_token
        else:
            raise AuthenticationFailed("User not authenticated")

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
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
class PostRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsSuperuserOrAuthor]
    authentication_classes = [CustomJWTAuthentication]
    # authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

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

