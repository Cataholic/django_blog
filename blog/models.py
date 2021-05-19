from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.html import strip_tags

import markdown


class Category(models.Model):
    name = models.CharField("分类", max_length=100)

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField("标签", max_length=100)

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField("标题", max_length=70)
    body = models.TextField("正文")
    author = models.ForeignKey(User, verbose_name="作者", on_delete=models.CASCADE)
    excerpt = models.CharField("摘要", max_length=200, blank=True)

    category = models.ForeignKey(Category, verbose_name="分类", on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name="标签", blank=True)

    created_time = models.DateTimeField("创建时间", default=timezone.now)
    modified_time = models.DateTimeField("修改时间")

    views = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        ordering = ["-created_time"]

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()

        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.excerpt = strip_tags(md.convert(self.body))[:54]

        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
