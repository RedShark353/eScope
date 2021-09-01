from django.shortcuts import render

from .models import Condition, Symptom

from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def allConditions(request):
    return render(request, "checker/index.html", {
        "conditions":Condition.objects.all()
    })

def conditionDetails(request, condition_id):
    condition = Condition.objects.get(pk=condition_id)
    symptomQuery = condition.main.all() | condition.secondary.all()
    allSymptoms = set()
    for symp in symptomQuery:
        allSymptoms.add(symp)
    return render(request, "checker/details.html", {
        "condition" : condition,
        "conditionSymptoms": allSymptoms
    })

def symptomForm(request):
    return render(request, "checker/symptomForm.html", {
        "allSymptoms":Symptom.objects.all()
    })

def symptomCheck(request):
    if request.method == "POST":
        symptoms = request.POST["symptomSet"]
        age = request.POST["age"]
        gender = request.POST["gender"]

        #Process results
        symptomArray = symptoms.split(",")
        del symptomArray[0]

        allPossibleConditions = set()
        allMatches = set()

        #Get all relevant conditions (main only)
        for symptom in symptomArray:
            sym = Symptom.objects.get(name=symptom)
            possible = Condition.objects.filter(main=sym)
            symptomSet = set(symptomArray) #All the patient's symptoms

            for cond in possible:
                allPossibleConditions.add(cond)

        #Add all the matches (main & secondary) to allMatches
        for s in symptomArray:
            sName = Symptom.objects.get(name=s)
            lessPossible = Condition.objects.filter(secondary=sName)
    
            for con in lessPossible:
                allMatches.add(con)
        allMatches = set.union(allPossibleConditions, allMatches)
        
        #Cross-check condition's main and patient's symptoms
        missingSymptomsList = []
        mostProbable = []
        for cond in allPossibleConditions:
            mainSymptomSet = set()
            mainSymptomsQuery = cond.main.all() #All the required symptoms of a condition
            condType = cond.type
            helpThreshold = 0.8

            for sympt in mainSymptomsQuery:
                mainSymptomSet.add(sympt.name)

            #Check if patient has the condition's main symptoms
            if condType == "AND":

                if mainSymptomSet.issubset(symptomSet):
                    mostProbable.append(cond)
                else:
                    #Help user
                    patientHas = mainSymptomSet.intersection(symptomSet)
                    missingRatio = len(patientHas) / len(mainSymptomSet)

                    if missingRatio >= helpThreshold:
                        missingSymptoms = mainSymptomSet - patientHas
                        missingSymptomsList.append(missingSymptoms)
                        
            else:
                if len(mainSymptomSet.intersection(symptomSet)):
                    mostProbable.append(cond)
        
            #Check for extra requirements:
            extraReq = cond.extra #Get extra reqs

            if extraReq:
                requirementElements = extraReq.split()
                #Analyze extras:
                if requirementElements[0] == "mainCount":
                    req = int(requirementElements[2])
                    #If the requirement is not met, remove from probable
                    if not (len(mainSymptomSet.intersection(symptomSet)) > req):
                        idx = mostProbable.index(cond)
                        mostProbable.pop(idx)

        #Check secondary to classify the most probable conditions
        sortingArray = []
        for condition in mostProbable:
            secondarySymptomQuery = condition.secondary.all() #All the secondary symptoms of a condition
            secondarySymptomSet = set()

            for sympt in secondarySymptomQuery:
                secondarySymptomSet.add(sympt.name)

            if len(secondarySymptomSet) > 0:
                intersectCount = len(secondarySymptomSet.intersection(symptomSet))
                secondaryRatio = intersectCount / len(secondarySymptomSet)
            else:
                secondaryRatio = 1 #This is if it has no secondary symptoms

            condTuple = (condition, round(secondaryRatio, 2))
            sortingArray.append(condTuple)

        sortingArray.sort(reverse=True, key=lambda tuple: tuple[1])

        return render(request, "checker/results.html", {
            "probable":sortingArray,
            "missing":missingSymptomsList,
            "lowAccuracy":allMatches - set(mostProbable), #without the probable
            "symptoms":symptomArray,
            "age":age,
            "gender":gender
        })

    else:
        return HttpResponseRedirect(reverse("form"))