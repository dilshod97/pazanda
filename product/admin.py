from django.contrib import admin
from .models import *


class FoodImageAdminInline(admin.TabularInline):
    model = FoodImages
    readonly_fields = ('id',)


class FoodAdmin(admin.ModelAdmin):
    list_display = ('name_uz',)
    inlines = (FoodImageAdminInline,)


admin.site.register(Category)
admin.site.register(Food, FoodAdmin)
