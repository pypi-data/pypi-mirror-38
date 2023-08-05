from django.contrib import admin
from script_codes.models import Script


@admin.register(Script)
class ScritpAdmin(admin.ModelAdmin):
    list_display = ['code', 'number', 'name']