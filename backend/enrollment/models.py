from django.db import models

SUBCOUNTY_CHOICES = [
    ('kajiado east', 'kajiado east'),
    ('kajiado west', 'kajiado west'),
    ('kajiado central', 'kajiado central'),
    ('kajiado north', 'kajiado north'),
    ('kajiado south', 'kajiado south'),
    ('mashuuru', 'mashuuru'),
    ('Oloililai', 'Oloililai')
]


class SchoolEnrollment(models.Model):
    uic_number = models.CharField(max_length=4, default='0000', primary_key=True)
    sub_county = models.CharField(max_length=20, choices=SUBCOUNTY_CHOICES)
    school_name = models.CharField(max_length=50)
    form1_boys = models.IntegerField()
    form1_girls = models.IntegerField()
    form1_all = models.IntegerField()
    form2_boys = models.IntegerField()
    form2_girls = models.IntegerField()
    form2_all = models.IntegerField()
    form3_boys = models.IntegerField()
    form3_girls = models.IntegerField()
    form3_all = models.IntegerField()
    form4_boys = models.IntegerField()
    form4_girls = models.IntegerField()
    form4_all = models.IntegerField()
    total_boys = models.IntegerField()
    total_girls = models.IntegerField()
    total_all = models.IntegerField()

    def __str__(self):
        return self.school_name + " uic: " + str(self.uic_number)
