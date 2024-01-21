from django.urls import path
from .views import *
urlpatterns=[
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("movies/", MovieView.as_view(), name="movies"),
    path("movies/<int:id>/", MovieView.as_view(), name="movies-id"),
    path("theater/", TheaterView.as_view(), name="theater"),
    path("theater/<int:id>/", TheaterView.as_view(), name="theater-id"),
    path("seat/",SeatsView.as_view(), name="seat"),
    path("seat/<int:id>/",SeatsView.as_view(), name="seat"),
    path("movie-theater/", MovieTheaterView.as_view(), name="movie-theater"),
    path("movie-theater/<int:movie_id>/", MovieTheaterView.as_view(), name="movie-theater"),
    path("theater-seat/", TheaterSeatView.as_view(), name="theater-seat"),
    path("theater-seat/<int:theater_id>/", TheaterSeatView.as_view(), name="theater-seat"),
    path("booking/", BookingView.as_view(), name="booking"),
    path("booking/<int:id>/", BookingView.as_view(), name="booking"),







]