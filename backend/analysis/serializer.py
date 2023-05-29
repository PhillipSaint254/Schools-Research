from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = "__all__"

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_authentication(self, obj):
        return obj.is_authenticated()


class SchoolRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationOfSchoolsData
        fields = '__all__'
        read_only_fields = ('uic_number',)


class SchoolInfrastructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolsInfrastructureStatus
        fields = '__all__'
        read_only_field = ('uic_number',)
