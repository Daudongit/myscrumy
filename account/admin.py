from django.contrib import admin
from .models import ScrumUser, Company

admin.site.register(ScrumUser)

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Company, CompanyAdmin)