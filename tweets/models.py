from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    content = models.TextField(max_length=280)
    add_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:20]

    @property
    def number_of_comments(self):
        return Comment.objects.filter(post=self).count()

    @property
    def url(self):
        return f"/tweet/{self.pk}/"


class Comment(models.Model):
    content = models.TextField(max_length=280)
    add_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:20]

    class Meta:
        ordering = ['-add_date']


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile',
                                on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, default="user.png")

    def __str__(self):
        return self.user.username

    @property
    def number_of_followers(self):
        return Follow.objects.filter(follow_user=self.user).count()

    @property
    def number_of_following(self):
        return Follow.objects.filter(user=self.user).count()


class Follow(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    follow_user = models.ForeignKey(User, related_name='follow_user', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
