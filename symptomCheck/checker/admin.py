from django.contrib import admin
from .models import Condition, Symptom

#Customization
class ConditionAdmin(admin.ModelAdmin):
    filter_horizontal = ("main", "secondary")

# Register your models here.
admin.site.register(Symptom)
admin.site.register(Condition, ConditionAdmin)
