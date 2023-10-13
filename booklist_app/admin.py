from django.contrib import admin
from .models import Book  # Import mô hình Book từ module models

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "description"]
