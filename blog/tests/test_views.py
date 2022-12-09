from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
import json

from ..models import Post
from ..serializers import BlogPostListSerializer
from core.views import BlogPostDetailSerializer
User = get_user_model()

client = Client()


class GetAllPostTest(TestCase):
    def setUp(self):
        author = User.objects.create(username='author #1')
        Post.objects.create(title='Blog Post #1',
                            text='Dummy text #1',
                            author=author)
        Post.objects.create(title='Blog Post #2',
                            text='Dummy text #2',
                            author=author)
        Post.objects.create(title='Blog Post #3',
                            text='Dummy text #3',
                            author=author)

    def test_get_all_posts(self):
        response = client.get(reverse('post_list'))
        posts = Post.objects.all()
        serializer = BlogPostListSerializer(posts, many=True)
        self.assertEqual(response.data, serializer.data)
        self.aasertEqual(response.status_code, status.HTTP_200_OK)


class GetSinglePostTest(TestCase):
    def setUp(self):
        author = User.objects.create(username='test')
        self.post = Post.objects.create(title='Blog Post #1', author=author)

    def test_get_valid_single_post(self):
        response = client.get(
            reverse('post_detail', kwargs={'id': self.post.id}))
        post = Post.objects.get(id=self.post.id)
        serializer = BlogPostDetailSerializer(post)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_0K)

    def test_get_invalid_single_post(self):
        response = client.get(reverse('post_detail', kwargs={'id': 9999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateSinglePostTest(TestCase):
    def setUp(self):
        self.author = User.objects.create(username='test')
        self.post = Post.objects.create(title='Blog Post #1',
                                        text='Post Description',
                                        author=self.author)
        self.valid_payload = {
            'title': 'Blog Post #1',
            'text': 'Blog Post Description',
            'author': 1,
        }
        self.invalid_payload = {
            'title': 'Blog Post #1',
            'text': None,
            'author': 1
        }

    def test_valid_update_post(self):
        response = client.put(reverse('post_detail',
                                      kwargs={'id': self.post.id}),
                              data=json.dumps(self.valid_payload),
                              content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_update_post(self):
        response = client.put(reverse('post_detail',
                                      kwargs={'id': self.post.id}),
                              data=json.dumps(self.invalid_payload),
                              content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeleteSinglePostTest(TestCase):
    def setUp(self):
        self.author = User.objects.create(username='test')
        self.post = Post.objects.create(title='Blog Post #1',
                                        text='Post Description',
                                        author=self.author)

    def test_valid_delete_post(self):
        response = client.delete(
            reverse('post_detail', kwargs={'id': self.post.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_delete_post(self):
        response = client.delete(reverse('post_detail', kwargs={'id': 9999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PublishSinglePostTest(TestCase):
    def setUp(self):
        self.api = APIClient()
        self.author = User.objects.create(username='test', password='test')
        self.post = Post.objects.create(title='Blog Post #1',
                                        text='Post Description',
                                        author=self.author,
                                        is_published=False)

    def test_unauth_publish_post(self):
        response = client.post(reverse('post_publish', args=[self.post.id]))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_authenticated_publish_post(self):
        self.api.force_authenticate(user=self.author)
        response = self.api.post(reverse('post_publish', args=[self.post.id]))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        post = Post.objects.get(title='Blog Post #1')
        self.assertEqual(post.is_published, True)