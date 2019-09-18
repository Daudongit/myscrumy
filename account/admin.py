from django.contrib import admin
from .models import ScrumUser, Company

class ScrumUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(ScrumUser, ScrumUserAdmin)
admin.site.register(Company, CompanyAdmin)