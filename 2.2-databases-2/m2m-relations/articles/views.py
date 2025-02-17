from django.shortcuts import render

from articles.models import Article


def articles_list(request):
    template = 'articles/news.html'
    ordering = request.GET.get('ordering', '-published_at')
    articles = Article.objects.prefetch_related('scopes').order_by(ordering)
    context = { 'articles': articles }
    return render(request, template, context)
