from rest_framework import serializers
from .models import Post
from django.contrib.auth.models import User



# class AuthorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'email']

# class AuthorListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username']

# class PostSerializer(serializers.ModelSerializer):
#     author = AuthorListSerializer( read_only=True)
#     # author = AuthorSerializer(read_only=True)
#     class Meta:
#         model = Post
#         fields = ['id', 'title', 'body', 'author']

# class PostDetailsSerializer(serializers.ModelSerializer):
#     author = AuthorSerializer( read_only=True)
#     # author = AuthorSerializer(read_only=True)
#     class Meta:
#         model = Post
#         fields = ['id', 'title', 'body', 'author']


class AuthorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class AuthorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'author']
    def get_author(self, obj):
        # Determine the request type (list or detail)
        is_list_request = self.context.get('is_list_request', False)

        # Choose the appropriate serializer based on the request type
        if is_list_request:
            author_serializer = AuthorListSerializer(obj.author)
        else:
            author_serializer = AuthorDetailSerializer(obj.author)

        return author_serializer.data
   