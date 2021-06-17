from django.contrib import admin

# Import všech modelů, které obsahuje models.py
from django.db.models import Count
from django.utils.html import format_html

from .models import *

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "book_count")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _book_count=Count("book", distinct=True),
        )
        return queryset

    def book_count(self, obj):
        return obj._book_count

    book_count.admin_order_field = "_book_count"
    book_count.short_description = "Počet knih"


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "birth_date")

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "release_year", "rate_percent", "pages_min")

    def release_year(self, obj):
        return obj.release_date.year

    def rate_percent(self, obj):
        return format_html("<b>{} %</b>", int(obj.rate * 10))

    def pages_min(self, obj):
        return format_html("<mark>{} </mark>", obj.pages)

    rate_percent.short_description = "Hodnocení knihy"
    release_year.short_description = "Rok uvedení"
    pages_min.short_description = "Počet stran"


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "filesize", "book_title")

    def book_title(self, obj):
        return obj.book.title



