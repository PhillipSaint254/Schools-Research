from django.db import models

WATER_SOURCE_CHOICES = [
    ('river/lake', 'river/lake'),
    ('rain taped', 'rain taped'),
    ('piped/taps', 'piped/taps'),
    ('borehole/well/dam', 'borehole/well/dam'),
    ('others', 'others')
]
SUBCOUNTY_CHOICES = [
    ('isinya', 'isinya'),
    ('kajiado west', 'kajiado west'),
    ('kajiado central', 'kajiado central'),
    ('kajiado north', 'kajiado north'),
    ('loitokitok', 'loitokitok'),
    ('mashuuru', 'mashuuru'),
    ('oloililai', 'oloililai')
]
POWER_SOURCE_CHOICES = [
    ('solar', 'solar'),
    ('mains electricity', 'mains electricity'),
    ('generator', 'generator'),
    ('others', 'others')
]
SECURITY_CHOICES = [
    ('fenced with gate', 'fenced with gate'),
    ('fenced with no gate', 'fenced with no gate'),
    ('no fence no gate', 'no fence no gate'),
    ('others', 'others')
]
CATEGORY_CHOICES = [
    ("public", 'Public'),
    ("private", 'Private'),
]
GENDER_CHOICES = [
    ("boys", 'boys'),
    ("girls", 'girls'),
    ('mixed', 'mixed')
]
TYPE_CHOICES = [
    ('day', 'day'),
    ('boarding', 'boarding'),
    ('day and boarding', 'day and boarding')
]
REGISTRATION_CHOICES = [
    ('full registration', 'full registration'),
    ('provincial registration', 'provincial registration'),
    ('re-registration', 're-registration')
]
SCHOOL_LEVEL_CHOICE = [
    ('ecde and primary', 'ecde and primary'),
    ('primary only', 'primary only'),
    ('junior secondary', 'junior secondary'),
    ('secondary', 'secondary')
]


class RegistrationOfSchoolsData(models.Model):
    time_stamp = models.DateTimeField()
    uic_number = models.CharField(max_length=4, default='0000', primary_key=True)
    name_of_school = models.CharField(max_length=50, null=True, default="")
    registration_number = models.IntegerField(null=True)
    date_of_registration = models.DateField()
    category = models.CharField(max_length=10, null=True, default="")
    gender_category = models.CharField(max_length=10, null=True, default="")
    level_of_school = models.CharField(max_length=30, default="", null=True)
    sub_county = models.CharField(max_length=20, default="", null=True)
    registration_status = models.CharField(max_length=50, default="", null=True)
    accommodation_category = models.CharField(max_length=20, null=True, default="")
    teacher_email = models.EmailField(null=True, default="")

    def __str__(self):
        return self.name_of_school + " uic: " + str(self.uic_number)


class SchoolsInfrastructureStatus(models.Model):
    uic_number = models.CharField(max_length=4, default='0000', primary_key=True)
    name_of_school = models.CharField(max_length=50)
    time_stamp = models.DateTimeField()
    boys_enrollment = models.IntegerField()
    girls_enrollment = models.IntegerField()
    total_enrollment = models.IntegerField()
    number_of_permanent_classrooms = models.IntegerField()
    number_of_temporary_classrooms = models.IntegerField()
    number_of_boys_toilets = models.IntegerField()
    number_of_girls_toilets = models.IntegerField()
    number_of_staff_toilets = models.IntegerField()
    number_of_taps = models.IntegerField()
    water_source = models.CharField(max_length=100)
    other_water_sources = models.TextField(null=True)
    power_source = models.CharField(max_length=20)
    other_power_sources = models.TextField(null=True)
    internet_connectivity = models.BooleanField(default=False)
    security = models.CharField(max_length=30)
    other_security = models.TextField(null=True)
    teacher_email = models.EmailField(null=True)
    comment = models.TextField()

    def __str__(self):
        return self.name_of_school + " uic: " + str(self.uic_number)
