from django.urls import path
from .views import *

app_name = 'enrollment'

urlpatterns = [
    path('school_enrollment/', get_school_enrollment, name='school_enrollment')
]
