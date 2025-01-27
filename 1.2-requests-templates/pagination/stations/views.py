from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
import csv
from django.core.paginator import Paginator


def index(request):
    return redirect(reverse("bus_stations"))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице

    with open(settings.BUS_STATION_CSV, encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)

    paginator = Paginator(data, 10)
    page_number = request.GET.get("page")

    page = paginator.get_page(page_number)

    context = {
        # "bus_stations": data,
        "page": page,
    }
    return render(request, "stations/index.html", context)
