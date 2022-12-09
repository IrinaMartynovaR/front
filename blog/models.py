from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from .managers import PostPublishedManager, PostManager
from django.template.defaultfilters import truncatewords
from django.shortcuts import get_object_or_404


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    title = models.CharField(max_length=200, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст статьи")
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    published_date = models.DateTimeField(blank=True, null=True, verbose_name="Дата публикации")
    is_published = models.BooleanField(default=False, verbose_name="Запись опубликована?")
    objects = PostManager()
    published = PostPublishedManager()

    def post_detail(request, id):
        post = get_object_or_404(Post, id=id)
        if not post.is_publish() and not request.user.is_staff:
            raise Http404('Запись в блоге не найдена')
        return render(request, 'blog/post_detail.html', {'post': post})

    def get_text_preview(self):
        return truncatewords(self.text, 10)

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def is_publish(self):
        return True if self.published_date else False

    def publish(self):
        self.published_date = timezone.now()
        self.is_published = True
        self.save()

    class Meta:
        verbose_name = "Запись в блоге"
        verbose_name_plural = "Записи в блоге"

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post',
                             on_delete=models.CASCADE,
                             related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField(verbose_name="Комментарий")
    created_date = models.DateTimeField(auto_now_add=True,  # default=timezone.now
                                        verbose_name='Дата создания')
    approved_comment = models.BooleanField(default=False,
                                           verbose_name='Одобрен?')

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарий'
