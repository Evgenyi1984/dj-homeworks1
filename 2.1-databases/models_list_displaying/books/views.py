from django.shortcuts import render
from .models import Book


def books_view(request):
    template = "books/books_list.html"
    books = Book.objects.all().order_by("pub_date")
    context = {"books": books}
    return render(request, template, context)


def books_by_date_view(request, pub_date):
    template = "books/books_list.html"
    books = Book.objects.filter(pub_date=pub_date)
    prev_date = (
        Book.objects.filter(pub_date__lt=pub_date)
        .order_by("-pub_date")
        .values_list("pub_date", flat=True)
        .first()
    )
    next_date = (
        Book.objects.filter(pub_date__gt=pub_date)
        .order_by("pub_date")
        .values_list("pub_date", flat=True)
        .first()
    )

    context = {"books": books, "prev_date": prev_date, "next_date": next_date}
    return render(request, template, context)
