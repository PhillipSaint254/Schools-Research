from django.contrib import admin
from .models import *


@admin.register(RegistrationOfSchoolsData)
class RegistrationOfSchoolsAdmin(admin.ModelAdmin):
    search_fields = ("name_of_school", "uic_number", 'sub_county', 'category')


@admin.register(SchoolsInfrastructureStatus)
class SchoolInfrastructureAdmin(admin.ModelAdmin):
    search_fields = ("name_of_school", "uic_number", 'sub_county', 'category')
