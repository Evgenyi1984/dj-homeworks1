from django.shortcuts import get_object_or_404, render, redirect
from .models import Phone


def index(request):
    return redirect("catalog")


def show_catalog(request):

    phones = Phone.objects.all()
    sort_param = request.GET.get("sort")

    if sort_param == "min_price":
        phones = phones.order_by("price")
    elif sort_param == "max_price":
        phones = phones.order_by("-price")
    else:
        phones = phones.order_by("name")

    template = "catalog.html"
    context = {"phones": phones}
    return render(request, template, context)


def show_product(request, slug):
    template = "product.html"
    phone = get_object_or_404(Phone, slug=slug)
    context = {'phone': phone}
    return render(request, template, context)
