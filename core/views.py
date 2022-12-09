from rest_framework import viewsets, serializers
from blog.models import Comment, Post
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

#import blog.serializers
from blog.serializers import CommentSerializer, BlogPostListSerializer




class ActionSerializedViewSet(viewsets.ModelViewSet):
    action = {}
    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]

        return self.serializer_class


class BlogPostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ()


class BlogPostDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()

    def get_comments_count(self, obj):
        return obj.comments.count()

    class Meta:
        model = Post
        fields = ('author', 'title', 'text', 'published_date', 'comments', 'comments_count')



class BlogPostViewSet(ActionSerializedViewSet):
    serializer_class = BlogPostListSerializer
    queryset = Post.objects.all()

    action_serializers = {
    'list':  BlogPostListSerializer,
    'retrieve': BlogPostDetailSerializer,
    'create': BlogPostCreateUpdateSerializer,
    'update': BlogPostCreateUpdateSerializer,
    }
    def get_queryset(self):
        queryset = self.queryset
        author = self.request.query_params.get('author', None)
        if author:
            queryset = queryset.filter(author_username=author)
        return queryset


    @action(detail=False)
    def published_posts(self, request):
        published_posts = Post.published.all()
        page = self.paginate_queryset(published_posts)
        if page is not None:
            serializers = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializers.data)

        serializer = self.get_serializer(published_posts, many=true)
        return Response(serializer.data)

    @action(detail=True,
            methods=['post'],
            permission_classes=[IsAuthenticated])
    def publish(self, request, id=None):
        post = self.get_object()
        if request.user == post.author:
            return Response({'message': 'blog post was published'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You don\t have permission'},
                            status=status.HTTP_403_FORBIDEN)