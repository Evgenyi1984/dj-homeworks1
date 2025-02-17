from django.contrib import admin
from django.forms import BaseInlineFormSet, ValidationError
from .models import Article, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()

        # пример данных в cleaned_data:
        # {
        #     'article': <Article: В "Детском мире" на Любянке открыли музей>,
        #     'tag': <Tag: Город>,
        #     'is_main': False,
        #     'id': <Scope: В "Детском мире" на Любянке открыли музей - Город>,
        #     'DELETE': False
        # }

        main_tag_found = False
        for form in self.forms:
            data = form.cleaned_data
            # пропускаем пустые формы и удаление
            if not data or data.get("DELETE"):
                continue
            # проверяем главный тэг
            if data.get("is_main", False):
                if main_tag_found:
                    raise ValidationError("Более одного тэга помечены как основные")
                main_tag_found = True
        if not main_tag_found:
            raise ValidationError("Ни один тэг не помечен как основной")


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]
