from django.urls import path

from .views import (
    add_tweet,
    add_comment,
    follow,
    search,

    home,
    post_view,
    user_view,
    settings_view,
)

urlpatterns = [
    path('', home, name='home_view'),

    path('tweet/new/', add_tweet, name='add_tweet'),
    path('tweet/<int:pk>/', post_view, name='post_view'),

    path('comment/add/<id>', add_comment, name='add_comment'),

    path('user/<user>/', user_view, name='user_view'),

    path('settings/', settings_view, name="settings"),

    path('follow/<int:followed>/<int:follower>/', follow, name="follow"),
    path('search/', search, name="search"),
]
