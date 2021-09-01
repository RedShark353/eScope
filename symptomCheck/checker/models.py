from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import IntegerField

#Options:
TYPE_OPTIONS = [
    ("AND", "AND"),
    ("OR", "OR")
]

# Create your models here.
class Symptom(models.Model):
    name = models.CharField(max_length=100)

    #This method returns the data as a str
    def __str__(self):
        return f"{self.name}"

class Condition(models.Model):
    name = models.CharField(max_length=100)
    main = models.ManyToManyField(Symptom, blank=False, related_name="mainSymptom")
    secondary = models.ManyToManyField(Symptom, blank=True, related_name="secondarySymptom")
    type = models.CharField(max_length=10, choices=TYPE_OPTIONS, default="AND")
    extra = models.CharField(max_length=64, blank=True)

    #This method returns the data as a str
    def __str__(self):
        return f"{self.name}"

#Superuser: usefu
#email: poponelson@outlook.com
#pass: Super...1.