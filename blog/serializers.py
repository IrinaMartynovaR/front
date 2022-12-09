from rest_framework import serializers
from .models import Post, Comment
from django import forms


from rest_framework import serializers

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'#('id', 'created_date', 'text', 'approve')


class BlogPostListSerializer(serializers.ModelSerializer):
    preview_text = serializers.SerializerMethodField()

    def get_preview_text(self, post):
        return post.get_text_preview()

    class Meta:
        model = Post
        fields = '__all__' #('title', 'author', 'created_date', 'preview_text')
