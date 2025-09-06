from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

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
    if not request.user.is_authenticated:
        login_url = reverse("login")
        return redirect(f"{login_url}?next={request.path}")
    movie = get_object_or_404(Movie, id=movie_id)
    seat = get_object_or_404(Seat, id=seat_id)

    ticket_exists = Ticket.objects.filter(movie=movie, seat=seat).exists()
    if not ticket_exists:
        Ticket.objects.create(movie=movie, seat=seat, user=request.user)

    return redirect("list_seats", movie_id=movie.id)


def stats(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Access Denied")

    seat_stats = (
        Ticket.objects.values("seat__number")
        .annotate(total=Count("id"))
        .order_by("seat__number")
    )

    return JsonResponse({"stats": list(seat_stats)})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})
