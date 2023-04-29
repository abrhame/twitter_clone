# def home(request):
#     return HttpResponse("Home page " + str(request.user))
from allauth.account.signals import user_signed_up
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.dispatch import receiver
from django.shortcuts import render, redirect

from tweets.models import UserProfile, Post, Comment, Follow


@login_required(redirect_field_name='account_login')
def home(request):
    tweets = Post.objects.filter(
        author__follow_user__user=request.user) | Post.objects.filter(author=request.user).order_by('-add_date')

    paginator = Paginator(tweets, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "user_info": request.user,
        "user_profile": UserProfile.objects.get(user=request.user),
        "tweets": page_obj,
    }
    return render(request, 'feed/home.html', context)


@login_required(redirect_field_name='account_login')
def post_view(request, pk):
    context = {
        "user_info": request.user,
        "user_profile": UserProfile.objects.get(user=request.user),
        "tweet": Post.objects.get(pk=pk),
        "pk": pk,
    }
    return render(request, 'feed/post.html', context)


@login_required(redirect_field_name='account_login')
def user_view(request, user):
    user = User.objects.get(username=user)
    tweets = Post.objects.filter(author=user).order_by("-add_date")
    paginator = Paginator(tweets, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "user_info": user,
        "user_profile": UserProfile.objects.get(user=user),
        "tweets": page_obj,
        "following": len(Follow.objects.filter(user=request.user).filter(follow_user=user)),
    }
    return render(request, 'feed/user.html', context)


@login_required(redirect_field_name='account_login')
def settings_view(request):
    user = request.user

    if request.method == "POST":
        if user.username != request.POST.get('username'):
            if not len(User.objects.filter(username__exact=request.POST.get('username'))):
                request.user.username = request.POST.get('username')

        if user.email != request.POST.get('email'):
            if not len(User.objects.filter(email__exact=request.POST.get('email'))):
                request.user.email = request.POST.get('email')

        if request.FILES:
            UserProfile(avatar=request.FILES['avatar'], user=user).save()

    user.profile.save()
    user.save()
    context = {
        "user_info": user,
        "user_profile": UserProfile.objects.get(user=user),

    }
    return render(request, 'feed/settings.html', context)


@receiver(user_signed_up)
def add_UserProfile(user, **kwargs):
    profile = UserProfile(user=user)
    profile.save()


@login_required(redirect_field_name='account_login')
def add_tweet(request):
    tweet = Post(content=request.POST.get('content'), author=request.user)
    tweet.save()
    return redirect('home_view')


@login_required(redirect_field_name='account_login')
def add_comment(request, id):
    comment = Comment(content=request.POST.get('content'), author=request.user, post=Post.objects.get(pk=id))
    comment.save()

    return redirect('post_view', pk=id)


@login_required(redirect_field_name='account_login')
def follow(request, followed, follower):
    follower = User.objects.get(id=follower)
    followed = User.objects.get(id=followed)

    obj = Follow.objects.filter(user=follower).filter(follow_user=followed)
    if obj:
        obj.delete()
    else:
        Follow(user=follower, follow_user=followed).save()

    return redirect('user_view', followed)


@login_required(redirect_field_name='account_login')
def search(request):
    results = User.objects.filter(username__icontains=request.POST.get("search"))
    context = {
        "user_info": request.user,
        "user_profile": UserProfile.objects.get(user=request.user),
        "results": results,
    }
    return render(request, 'feed/results.html', context)
