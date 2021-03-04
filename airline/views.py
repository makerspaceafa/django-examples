from django import forms
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseBadRequest, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from .models import Flight, Passenger


# Create your views here.
def index(request):
    return render(request, "airline/index.html", {
        "flights": Flight.objects.all()
    })


def user(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("airline:login"))
    return render(request, "airline/user.html")


def flight(request, flight_id):
    try:
        flight = Flight.objects.get(id=flight_id)
    except Flight.DoesNotExist:
        raise Http404("Flight not found.")
    return render(request, "airline/flight.html", {
        "flight": flight,
        "passengers": flight.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
    })


def book(request, flight_id):
    if request.method == "POST":
        try:
            passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))
            flight = Flight.objects.get(pk=flight_id)
        except KeyError:
            return HttpResponseBadRequest("Bad Request: no flight chosen")
        except Flight.DoesNotExist:
            return HttpResponseBadRequest("Bad Request: flight does not exist")
        except Passenger.DoesNotExist:
            return HttpResponseBadRequest("Bad Request: passenger does not exist")
        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse("airline:flight", args=(flight_id,)))


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("airline:index"))
        else:
            return render(request, "airline/login.html", {
                "message": "Invalid credentials."
            })
    else:
        return render(request, "airline/login.html")


def logout_view(request):
    logout(request)
    return render(request, "airline/login.html", {
        "message": "Logged out."
    })