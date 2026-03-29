from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.createGame, name="create_game"),
    path("play/", views.play, name="play"),
    path("review/<int:id>/<int:move>", views.review, name="review"),
]