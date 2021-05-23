import os
import sys
import random
import pathlib
from datetime import timedelta

import django
import faker
from django.utils import timezone

back = os.path.dirname
BASE_DIR = back(back(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_blog.settings.local')
    django.setup()

    from blog.models import Post, Category, Tag
    from comments.models import Comment
    from django.contrib.auth.models import User

    print('clean database')
    Post.objects.all().delete()
    Category.objects.all().delete()
    Tag.objects.all().delete()
    Comment.objects.all().delete()
    User.objects.all().delete()

    print('create a blog user')
    user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin')
    category_list = ['test category1', 'test category2', 'test category3', 'test category4']
    tag_list = ['test tag1', 'test tag2', 'test tag3', 'test tag4']
    a_year_aog = timezone.now() - timedelta(days=365)

    print('create categories and tags')
    for cate in category_list:
        Category.objects.create(name=cate)

    for tag in tag_list:
        Tag.objects.create(name=tag)

    print('create a markdown sample post')
    Post.objects.create(
        title='Markdown 与代码高亮测试',
        body=pathlib.Path(BASE_DIR).joinpath('scripts', 'md.sample').read_text(encoding='utf-8'),
        category=Category.objects.create(name='Markdown测试'),
        author=user,
    )

    print('create some faked posts published whthin the past year')
    fake = faker.Faker('zh_CN')
    for _ in range(100):
        tags = Tag.objects.all().order_by('?')
        tag1 = tags.first()
        tag2 = tags.last()
        cate = Category.objects.all().order_by('?').first()
        created_time = fake.date_time_between(start_date='-1y', end_date='now', tzinfo=timezone.get_current_timezone())
        post = Post.objects.create(
            title=fake.sentence().rstrip('.'),
            body='\n\n'.join(fake.paragraphs(10)),
            created_time=created_time,
            category=cate,
            author=user,
        )
        post.tags.add(tag1, tag2)
        post.save()

    print('create some comments')
    for post in Post.objects.all()[:20]:
        post_created_time = post.created_time
        delta_in_days = '-' + str((timezone.now() - post_created_time).days) + 'd'
        for _ in range(random.randrange(3, 15)):
            Comment.objects.create(
                name=fake.name(),
                email=fake.email(),
                url=fake.url(),
                text=fake.paragraph(),
                created_time=fake.date_time_between(
                    start_date=delta_in_days,
                    end_date='now',
                    tzinfo=timezone.get_current_timezone()),
                post=post,
            )
    print('done!')
