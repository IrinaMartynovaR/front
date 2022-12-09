from django import forms

from .models import Post, Comment
from rest_framework import serializers


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'is_published')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class BlogPostListSerializer(serializers.ModelSerializer):
    preview_text = serializers.SerializerMethodField()

    def get_preview_text(self, post):
        return post.get_text_preview()

    class Meta:
        model = Post
        fields = ('title', 'author', 'created_date', 'preview_text')
