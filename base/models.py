from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=160, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', default='default_profile_image.png')

class Tweet(models.Model):
    text = models.CharField(max_length=280)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='tweet_images/', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='liked_tweets')
    retweets = models.ManyToManyField(User, related_name='retweeted_tweets')

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    date_followed = models.DateTimeField(auto_now_add=True)

class DirectMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    message = models.CharField(max_length=280)
    date_sent = models.DateTimeField(auto_now_add=True)

class Reply(models.Model):
    tweet = models.ForeignKey('Tweet', on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s reply to {self.tweet.user.username}"

    def get_absolute_url(self):
        return reverse('tweet_detail', args=[str(self.tweet.id)])
class Notification(models.Model):
    recipient = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=50)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    message = models.ForeignKey(DirectMessage, on_delete=models.CASCADE, blank=True, null=True)
    date_sent = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
