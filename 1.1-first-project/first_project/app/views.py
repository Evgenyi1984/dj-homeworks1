from django.http import HttpResponse
from django.shortcuts import render, reverse
import datetime, os


def home_view(request):
    template_name = 'app/home.html'
    # впишите правильные адреса страниц, используя
    # функцию `reverse`
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время':reverse('time'),
        'Показать содержимое рабочей директории':reverse('workdir')
    }
    
    # context и параметры render менять не нужно
    # подбробнее о них мы поговорим на следующих лекциях
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    # обратите внимание – здесь HTML шаблона нет, 
    # возвращается просто текст
    time_now = datetime.datetime.now().time()
    modified_datetime = time_now.replace(microsecond=0)
    current_time = modified_datetime
    msg = f'Текущее время: {current_time}'
    return HttpResponse(msg)


def workdir_view(request):
    list_of_files = os.listdir()
    
   
    # по аналогии с `time_view`, напишите код,
    # который возвращает список файлов в рабочей 
    # директории
    return HttpResponse(', '.join(list_of_files))
