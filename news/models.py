from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Имя')
    rating =  models.IntegerField(default=0, verbose_name='Рейтинг')

    def update_rating(self):
        post_rating = self.post_set.aggregate(rating_sum=Sum('rating'))['rating_sum'] or 0
        author_com_rating = self.username.comment_set.aggregate(rating_sum=Sum('rating'))['rating_sum'] or 0
        post_com_rating = Comment.objects.filter(post__author=self).aggregate(rating_sum=Sum('rating'))['rating_sum'] or 0

        self.rating = (post_rating * 3) + author_com_rating + post_com_rating
        self.save()

    def __str__(self):
        return f'{self.username.username}'


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='Название')

    def __str__(self):
        return self.name


class Post(models.Model):
    news = 'NW'
    article = 'AR'

    TYPEPOST = [
        (news, 'Новость'),
        (article, 'Статья'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    type = models.CharField(max_length=2, choices=TYPEPOST, default='NW', verbose_name='Тип поста')
    date_add = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    category = models.ManyToManyField(Category, through='PostCategory', verbose_name='Категория')
    name = models.CharField(max_length=128, verbose_name='Название')
    text = models.TextField(verbose_name='Содержание')
    rating =  models.IntegerField(default=0, verbose_name='Рейтинг')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return (self.text[:124] + '...') if len(self.text) > 124 else self.text

    def __str__(self):
        return (f'{self.name} {self.author} {self.date_add} {self.category.name} '
                f'{self.type} {self.rating} {self.preview()}')

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField(verbose_name='Текст комментария')
    date_add = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    rating =  models.IntegerField(default=0, verbose_name='Рейтинг')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.text} {self.user.username} {self.date_add} {self.rating}'
