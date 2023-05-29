from datetime import datetime
import gspread
from django.core.checks import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from oauth2client.service_account import ServiceAccountCredentials
from django.http import JsonResponse
from rest_framework import generics
from .serializer import *
from .models import *
from .serializer import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class UserView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class SchoolRegistrationVIew(generics.ListAPIView):
    queryset = RegistrationOfSchoolsData.objects.all()
    serializer_class = SchoolRegistrationSerializer


class SchoolInfrastructureView(generics.ListAPIView):
    queryset = SchoolsInfrastructureStatus.objects.all()
    serializer_class = SchoolInfrastructureSerializer


class SchoolRegistrationSearchView(generics.ListAPIView):
    serializer_class = SchoolRegistrationSerializer

    def get_queryset(self):
        search_term = self.request.query_params.get('search')
        queryset = RegistrationOfSchoolsData.objects.filter(name_of_school__icontains=search_term)
        return queryset


class SchoolInfrastructureSearchView(generics.ListAPIView):
    serializer_class = SchoolInfrastructureSerializer

    def get_queryset(self):
        search_term = self.request.query_params.get('search')
        queryset = SchoolsInfrastructureStatus.objects.filter(name_of_school__icontains=search_term)
        return queryset


class GetSchoolByLevelView(View):
    def get(self, request):
        sub_county = request.GET.get('sub-county').strip()
        level = request.GET.get('level').upper().strip()

        if sub_county.lower() == "kajiado central":
            sub_county = "Kajiado Central"

        print("_____________________________________________________________________________________________________________-")
        print()
        print()
        print("sub county: '" + sub_county + "'")
        print("level: '" + level + "'")
        print()
        print()
        print("_____________________________________________________________________________________________________________-")

        if level == "ALL":
            schools = RegistrationOfSchoolsData.objects.filter(Q(sub_county__contains=sub_county))
        else:
            schools = RegistrationOfSchoolsData.objects.filter(
                Q(sub_county__contains=sub_county) & Q(level_of_school__contains=level))

        data = [{
            'uic_number': school.uic_number, 'name_of_school': school.name_of_school,
            'registration_number': school.registration_number, 'date_of_registration': school.date_of_registration,
            'category': school.category, 'gender_category': school.gender_category,
            'registration_status': school.registration_status, 'accommodation_category': school.accommodation_category
        } for school in schools]

        return JsonResponse({'data': data})


class GetRegisteredSchool(generics.RetrieveAPIView):
    serializer_class = SchoolRegistrationSerializer
    queryset = RegistrationOfSchoolsData.objects.all()
    lookup_field = 'uic_number'


class GetSchoolInfrastructureAnalysis(generics.RetrieveAPIView):
    serializer_class = SchoolInfrastructureSerializer
    queryset = SchoolsInfrastructureStatus.objects.all()
    lookup_field = 'uic_number'


def get_registered_schools(request):
    schools = RegistrationOfSchoolsData.objects.all()
    data = [{
        'uic_number': school.uic_number, 'name': school.name_of_school,
        'registration_number': school.registration_number, 'date_of_registration': school.date_of_registration,
        'category': school.category, 'gender_category': school.gender_category,
        'prov_or_full': school.provi_or_full, 'type': school.type
    } for school in schools]

    return JsonResponse({'data': data})


def get_schools_analysis(request):
    schools = SchoolsInfrastructureStatus.objects.all()
    data = [{
        'uic_number': school.uic_number, 'name': school.name_of_school, 'date': school.date,
        'number_of_boys': school.boys_enrollment, 'number_of_girls': school.girls_enrollment,
        'total_population': school.total_enrollment, 'number_of_permanent_classrooms': school.number_of_permanent_classrooms,
        'number_of_temporary_classrooms': school.number_of_temporary_classrooms, 'number_of_boys_toilets': school.number_of_boys_toilets,
        'number_of_girls_toilets': school.number_of_girls_toilets, 'number_of_staff_toilets': school.number_of_staff_toilets,
        'number_of_taps': school.number_of_taps, 'water_source': school.water_source, 'power_source': school.power_source,
        'internet_connectivity': school.internet_connectivity, 'security': school.security, 'comment': school.comment

    } for school in schools]

    return JsonResponse({'data': data})


def get_user(request):
    user = request.user

    if user.is_authenticated:
        data = {
            'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email
        }
    else:
        data = "False user authentication"

    return JsonResponse({"data": data})


def save_registration_data(request):
    # Set up credentials
    # Set up credentials
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'C:\\Users\\ABC\\Desktop\\work auto tools\\enrollment_and_analysis\\analysis\\key\\cridentials.json', scope)
    client = gspread.authorize(credentials)

    # Access the Google Sheets spreadsheet
    sheet = client.open("registration of schools form").sheet1  # Replace sheet1 with the actual sheet name
    # time stamp # uic # name # reg no # date of reg # reg status # email
    # accommodation category(type) # level of school # school category # sub county
    # for i in range(5):
    #     print("*" * i)
    for row in sheet.get_all_values()[1:]:
        try:
            school = RegistrationOfSchoolsData.objects.get(uic_number=row[1])
            flag = 0

            date_str = str(row[4])
            if date_str:
                parts = date_str.split("/")
                new_date = parts[2] + "-" + parts[1] + "-" + parts[0]
                date_obj = datetime.strptime(new_date, "%Y-%m-%d").date()
                school.date_of_registration = date_obj
                flag = 1
            if row[2]:
                school.name_of_school = row[2]
                flag = 1
            if row[3]:
                school.registration_number = row[3]
                flag = 1
            if row[5]:
                school.registration_status = row[5]
                flag = 1
            if row[6]:
                school.teacher_email = row[6]
                flag = 1
            if row[7]:
                school.accommodation_category = row[7]
                flag = 1
            if row[8]:
                school.level_of_school = row[8]
                flag = 1
            if row[9]:
                school.category = row[9]
                flag = 1
            if row[10]:
                school.sub_county = row[10]
                flag = 1

            timestamp_str = str(row[0])
            if timestamp_str and flag > 0:
                date, time = timestamp_str.split(" ")
                date_parts = date.split("/")
                new_date = date_parts[2] + "/" + date_parts[1] + "/" + date_parts[0] + " " + time
                timestamp = datetime.strptime(new_date, "%Y/%m/%d %H:%M:%S")
                school.time_stamp = timestamp
                school.save()

        except RegistrationOfSchoolsData.DoesNotExist:
            school = RegistrationOfSchoolsData(
                uic_number=row[1],
                name_of_school=row[2],
                registration_number=row[3],
                registration_status=row[5],
                teacher_email=row[6],
                accommodation_category=row[7],
                level_of_school=row[8],
                category=row[9],
                sub_county=row[10],
                gender_category=row[11]
            )
            timestamp_str = str(row[0])
            if timestamp_str:
                date, time = timestamp_str.split(" ")
                date_parts = date.split("/")
                new_date = date_parts[2] + "/" + date_parts[1] + "/" + date_parts[0] + " " + time
                timestamp = datetime.strptime(new_date, "%Y/%m/%d %H:%M:%S")
                school.time_stamp = timestamp

            date_str = str(row[4])
            if date_str:
                # User provided a date value, parse it and save
                parts = date_str.split("/")
                new_date = parts[2] + "-" + parts[1] + "-" + parts[0]
                date_obj = datetime.strptime(new_date, "%Y-%m-%d").date()
            else:
                # User did not provide a date value, use the current date
                date_obj = datetime.now().date()
            school.date_of_registration = date_obj
            school.save()

    return redirect("http://localhost:3000/")


def save_analysis_data(request):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'C:\\Users\\ABC\\Desktop\\work auto tools\\enrollment_and_analysis\\analysis\\key\\cridentials.json', scope)
    client = gspread.authorize(credentials)

    # Access the Google Sheets spreadsheet
    sheet = client.open("SCHOOL INFRUSTURE FORM (Responses)").sheet1  # Replace sheet1 with the actual sheet name

    # time stamp # email # school_name # uic # no of boys # no of girls # permanent class # temporary class
    # boys toilets # girls toilets # staff toilets # no of taps # water source # others water description
    # internet connectivity # source of electricity # electricity others description # security features
    # security other description # comment

    for row in sheet.get_all_values()[1:]:
        try:
            flag = 0
            school = SchoolsInfrastructureStatus.objects.get(uic_number=row[3])
            if row[1]:
                school.teacher_email = row[1]
                flag = 1
            if row[2]:
                school.name_of_school = row[2]
                flag = 1
            population = 0
            if row[4]:
                school.boys_enrollment = int(row[4])
                population += int(row[4])
                flag = 1
            if row[5]:
                school.girls_enrollment = int(row[5])
                population += int(row[4])
                flag = 1

            school.total_enrollment = population

            if row[6]:
                school.number_of_permanent_classrooms = int(row[6])
                flag = 1
            if row[7]:
                school.number_of_temporary_classrooms = int(row[7])
                flag = 1
            if row[8]:
                school.number_of_boys_toilets = int(row[8])
                flag = 1
            if row[9]:
                school.number_of_girls_toilets = int(row[9])
                flag = 1
            if row[10]:
                school.number_of_staff_toilets = int(row[10])
                flag = 1
            if row[11]:
                school.number_of_taps = int(row[11])
                flag = 1
            if row[12]:
                school.water_source = row[12]
                flag = 1
            if row[13] and row[12].lower() == "others":
                school.other_water_sources = row[13]
                flag = 1
            if row[14]:
                school.internet_connectivity = row[14].lower() == "yes"
                flag = 1
            if row[15]:
                school.power_source = row[15]
                flag = 1
            if row[16] and row[15].lower() == "others":
                school.other_power_sources = row[16]
                flag = 1
            if row[17]:
                school.security = row[17]
                flag = 1
            if row[18] and row[17].lower() == "others":
                school.other_security = row[18]
                flag = 1
            if row[19]:
                school.comment = row[19]
                flag = 1

            timestamp_str = str(row[0])
            if timestamp_str and flag > 0:
                date, time = timestamp_str.split(" ")
                date_parts = date.split("/")
                new_date = date_parts[2] + "/" + date_parts[1] + "/" + date_parts[0] + " " + time
                timestamp = datetime.strptime(new_date, "%Y/%m/%d %H:%M:%S")
                school.time_stamp = timestamp
                school.save()

        except SchoolsInfrastructureStatus.DoesNotExist:
            school = SchoolsInfrastructureStatus(
                teacher_email=row[1],
                name_of_school=row[2],
                uic_number=row[3],
            )
            population = 0
            if row[4]:
                school.boys_enrollment = int(row[4])
                population += int(row[4])

            if row[5]:
                school.girls_enrollment = int(row[5])
                population += int(row[4])

            school.total_enrollment = population

            if row[6]:
                school.number_of_permanent_classrooms = int(row[6])
            if row[7]:
                school.number_of_temporary_classrooms = int(row[7])
            if row[8]:
                school.number_of_boys_toilets = int(row[8])
            if row[9]:
                school.number_of_girls_toilets = int(row[9])
            if row[10]:
                school.number_of_staff_toilets = int(row[10])
            if row[11]:
                school.number_of_taps = int(row[11])
            if row[12]:
                school.water_source = row[12]
            if row[13]:
                school.other_water_sources = row[13]
            if row[14]:
                school.internet_connectivity = row[14].lower() == "yes"
            if row[15]:
                school.power_source = row[15]
            if row[16] and row[15].lower() == "others":
                school.other_power_sources = row[16]
            if row[17]:
                school.security = row[17]
            if row[18] and row[17].lower() == "others":
                school.other_security = row[18]
            if row[19]:
                school.comment = row[19]

            timestamp_str = str(row[0])
            if timestamp_str:
                date, time = timestamp_str.split(" ")
                date_parts = date.split("/")
                new_date = date_parts[2] + "/" + date_parts[1] + "/" + date_parts[0] + " " + time
                timestamp = datetime.strptime(new_date, "%Y/%m/%d %H:%M:%S")
                school.time_stamp = timestamp
            school.save()

        except ValueError:
            messages.Info(request, "User with school UIC '" + row[3] + "' entered invalid values for a required field.")
    return render(request, "analysis/success.html", {"data": sheet.get_all_values()})


def get_sub_county_data(request):
    data = []
    subcounties = ["Kajiado Central", "isinya", "loitokitok", "kajiado north", "kajiado west", "mashuuru", "oloililai"]
    total_schools = 0
    total_primary_with_ecd = 0
    total_primary_only = 0
    total_junior_secondary = 0
    total_secondary = 0

    for sub_county in subcounties:
        all_schools_in_sub_county = RegistrationOfSchoolsData.objects.filter(Q(sub_county__contains=sub_county)).count()
        all_primaries_with_ecd_in_sub_county = RegistrationOfSchoolsData.objects.filter(Q(sub_county__contains=sub_county) & Q(level_of_school__contains="ecde and primary")).count()
        all_primary_only_in_sub_county = RegistrationOfSchoolsData.objects.filter(Q(sub_county__contains=sub_county) & Q(level_of_school__contains="primary only")).count()
        all_junior_secondaries_in_sub_county = RegistrationOfSchoolsData.objects.filter(Q(sub_county__contains=sub_county) & Q(level_of_school__contains="junior secondary")).count()
        all_secondaries_in_sub_county = RegistrationOfSchoolsData.objects.filter(Q(sub_county__contains=sub_county) & Q(level_of_school__contains="secondary")).count()
        total_schools += all_schools_in_sub_county
        total_primary_only += all_primary_only_in_sub_county
        total_primary_with_ecd += all_primaries_with_ecd_in_sub_county
        total_junior_secondary += all_junior_secondaries_in_sub_county
        total_secondary += all_secondaries_in_sub_county
        data.append({
            "sub_county_name": sub_county,
            "number_of_schools_in_sub_county": all_schools_in_sub_county,
            "all_primaries_with_ecd": all_primaries_with_ecd_in_sub_county,
            "all_primary_only": all_primary_only_in_sub_county,
            "all_junior_secondary": all_junior_secondaries_in_sub_county,
            "all_secondary": all_secondaries_in_sub_county,
        })

    for counter in range(7):
        data[counter]["all_schools_in_county"] = total_schools
        data[counter]["all_primaries_with_ecd_in_county"] = total_primary_with_ecd
        data[counter]["all_primary_only_in_county"] = total_primary_only
        data[counter]["all_junior_secondary_in_county"] = total_primary_with_ecd
        data[counter]["all_secondary_in_county"] = total_primary_with_ecd
        data[counter]['image'] = "../img/img-" + str(counter + 1) + ".jpg"

    return JsonResponse({"data": data})
