from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Tweet, Reply, Profile
from .forms import TweetForm

def home(request):
    tweets = Tweet.objects.all().order_by('-created_at')[:10]
    context = {'tweets': tweets}
    return render(request, 'home.html', context)

@login_required
def new_tweet(request):
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('home')
    else:
        form = TweetForm()
    context = {'form': form}
    return render(request, 'new_tweet.html', context)

def profile(request, username):
    user = get_object_or_404(User, username=username)
    tweets = Tweet.objects.filter(user=user).order_by('-created_at')
    context = {'user': user, 'tweets': tweets}
    return render(request, 'profile.html', context)

def tweet_detail(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    replies = Reply.objects.filter(tweet=tweet).order_by('-created_at')
    context = {'tweet': tweet, 'replies': replies}
    return render(request, 'tweet_detail.html', context)

@login_required
def follow(request, username):
    user = get_object_or_404(User, username=username)
    follower = request.user.profile
    following = user.profile
    follower.following.add(following)
    return redirect('profile', username=username)
