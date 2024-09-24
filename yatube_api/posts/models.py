from django.contrib.auth import get_user_model
from django.db import models

from posts.constants import TITLE_MAX_LENGTH, TITLE_MAX_LENGTH_ADMIN

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title[:TITLE_MAX_LENGTH_ADMIN]

    class Meta:
        ordering = ('title',)


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True
    )
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)

    def __str__(self):
        return self.text[:TITLE_MAX_LENGTH]

    class Meta:
        ordering = ('-pub_date', 'group', 'author',)


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created', 'author',)


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='users')

    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followings')

    class Meta:
        ordering = ('following',)
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'following'),
                name='user_following_unique'
            ),
            models.CheckConstraint(
                check=models.Q(models.F('user') != models.F('following')),
                name='user_not_following'
            ),
        )
