from django.urls import path
from . import views

urlpatterns = [
    path("", views.symptomForm, name="form"),
    path("results/", views.symptomCheck, name="results"),
    path("<int:condition_id>", views.conditionDetails, name="details"),
    path("allConditions/", views.allConditions, name="allConditions")
]