from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("draw/", views.to_draw, name="draw"),
    path("save_to_gallery/", views.save_to_gallery, name="save_to_gallery"),
    path("gallery/", views.gallery, name="gallery"),
    path("showcase/", views.showcase, name="showcase"),
    path("saveopus/", views.saveopus, name="saveopus"),
    path("killopus/", views.killopus, name="killopus"),
    path("favorited/", views.favorited, name="favorited"),
    path("searchopus/", views.searchopus, name="searchopus"),
    path("deleteopus/", views.deleteopus, name="deleteopus"),
    path("profile/<str:created_by>/", views.profile, name="profile"),
    path('follow/<str:username>/', views.follow, name='follow'),
    path('unfollow/<str:username>/', views.unfollow, name='unfollow'),
    path("following/", views.following, name="following"),
 ]