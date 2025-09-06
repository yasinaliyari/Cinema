from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404
from app.models import Movie, Ticket, Seat


def list_movies(request):
    return render(request, "app/movies.html", {"movies": Movie.objects.all()})


def list_seats(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    reserved_seats = Ticket.objects.filter(movie=movie).values_list(
        "seat_id", flat=True
    )
    seats = Seat.objects.exclude(id__in=reserved_seats)

    return render(request, "app/seats.html", {"movie": movie, "seats": seats})


def reserve_seat(request, movie_id, seat_id):
    pass


def stats(request):
    pass


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})
