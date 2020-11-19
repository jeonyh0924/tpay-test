from django.contrib import admin

# Register your models here.
from shop.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
