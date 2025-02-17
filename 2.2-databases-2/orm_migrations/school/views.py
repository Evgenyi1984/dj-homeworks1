from django.views.generic import ListView
from django.shortcuts import render

from .models import Student


def students_list(request):
    template = 'school/students_list.html'
    ordering = request.GET.get('ordering', 'group')
    students = Student.objects.prefetch_related('teachers').order_by(ordering)
    context = { 'students': students, 'ordering': ordering }
    return render(request, template, context)
