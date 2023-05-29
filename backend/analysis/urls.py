from django.urls import path, re_path
from .views import *

app_name = 'analysis'

urlpatterns = [
    path('registered_schools/', SchoolRegistrationVIew.as_view(), name='registration_of_schools'),
    path('registered_schools/save_registration_data/', save_registration_data, name='save_registration_data'),
    path('registered_schools/data/', get_registered_schools, name='registration_of_schools_data'),
    path('registered_schools/get_school_by_level/', GetSchoolByLevelView.as_view(), name='get_school_by_level'),
    path('registered_schools/search/', SchoolRegistrationSearchView.as_view(), name='search_registered_schools'),  # New URL for search
    re_path(r'^registered_schools/get_school/(?P<uic_number>[a-zA-Z0-9]{4})/$', GetRegisteredSchool.as_view(), name='get_registered_school'),
    path('schools_infrastructure_status/', SchoolInfrastructureView.as_view(), name='school_infrastructure_status'),
    path('schools_infrastructure_status/save_analysis_data/', save_analysis_data, name='save_analysis_data'),
    path('schools_infrastructure_status/data/', get_schools_analysis, name='school_infrastructure_status_data'),
    path('schools_infrastructure_status/search/', SchoolInfrastructureSearchView.as_view(), name='search_schools_analysis'),  # New URL for search
    re_path(r'^schools_infrastructure_status/get_school/(?P<uic_number>[a-zA-Z0-9]{4})/$', GetSchoolInfrastructureAnalysis.as_view(), name='get_schools_infrastructure_status'),
    path('registered_schools/sub_county_data/', get_sub_county_data, name="sub_county_data")
]
