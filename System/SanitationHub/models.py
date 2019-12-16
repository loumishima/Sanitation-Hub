from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

from django.db import models
from stdimage.models import StdImageField

def generateRandomValue():
    import random, string

    return ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k = 6))

class Organisation(models.Model):
    name = models.CharField('Name', max_length=50)
    dateEntrance = models.DateField('Date of Creation', editable=False, auto_now_add=True)
    codeID = models.CharField('OrgID', unique=True, max_length=6, default = generateRandomValue)
    isHubMember = models.BooleanField('IsHubMember')

    def __str__(self):
        return self.name




class User(AbstractUser):
    dateEntrance = models.DateField('Date of Creation', editable=False, auto_now_add=True)
    profilePic = StdImageField('Profile Picture', variations={'thumb': (124,124)})
    organisation = models.ForeignKey(Organisation, on_delete='SET_NULL', blank=True, null=True)

    def __str__(self):
        return self.username

class Dataset(models.Model):
    filename = models.FileField('Filename', upload_to= 'dsfiles/')
    dateUploaded = models.DateField('Date of Creation', editable=False, auto_now=True)
    ipAddress = models.GenericIPAddressField('IpAdd', blank=True, null=True )
    latitude = models.FloatField('latitude', blank=True, null=True)
    longitude = models.FloatField('longitude',blank=True,null=True)
    organisation = models.ForeignKey(Organisation, on_delete='cascade', blank=True,null=True,related_name='+')

class StatsResumed(models.Model):
    number_toilets = models.IntegerField('Number of toilets', blank=True, null=True)
    capacity_mean = models.FloatField('Capacity Avg', blank=True, null=True)
    capacity_std = models.FloatField('Capacity Stdev', blank=True, null=True)
    people_using_max = models.FloatField('Usage Max', blank=True, null=True)
    people_using_min = models.FloatField('Usage Min', blank=True, null=True)
    people_using_mean = models.FloatField('Usage Mean', blank=True, null=True)
    people_using_std = models.FloatField('Usage Stdev', blank=True, null=True)
    last_cleaned_max = models.FloatField('Cleaning time Max', blank=True, null=True)
    last_cleaned_min = models.FloatField('Cleaning time Min', blank=True, null=True)
    last_cleaned_max = models.FloatField('Cleaning time Mean', blank=True, null=True)
    last_cleaned_max = models.FloatField('Cleaning time Stdev', blank=True, null=True)


    