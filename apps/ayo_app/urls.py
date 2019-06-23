from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login),
    url(r'^home$', views.index),
    url(r'^credits$', views.credits),
    url(r'^game$', views.game),
    url(r'^leaderboard$', views.leaderboard),
    url(r'^register$', views.addUser),
    url(r'^login$', views.loginUser),
    url(r'^logout$', views.logout),
    url(r'^tutorial$', views.tutorial),
]
