from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.conf import settings
import json
from homepages.models import Food, Nutrient, Patient, Alert, Nutrient_In_Food, Patient_Logs_Food, Measurement, Patient_Condition, Condition, Patient_Favorite_Food, Alert_Type
from datetime import datetime as dt

loggedIn = False
loggedInUsername = ""
loggedInPatientId = None

def indexPageView(request):
    global loggedInPatientId
    global loggedInUsername

    """
    # Recommended Daily Amounts:
    Protein                         0.6 g / kg
    Potassium, K                    3000 mg
    Carbohydrate, by difference     250 g
    Sodium, Na                      2300 mg
    Water                           3700 mg
    Phosphorus, P                   3500 mg
    Sugar                           30 g
    """

    if loggedInPatientId != None:
        patientData = Patient.objects.get(id = loggedInPatientId)
        nutrientData = Nutrient.objects.all()
        
        # Filter Nutrient Data down to the logged in users nutrients from today
        allNutrientInFoodData = Nutrient_In_Food.objects.all()


        loggedFoods = Patient_Logs_Food.objects.all()
        nutrients = []

        currentProteinAmount = 0
        currentPotassiumAmount = 0
        currentCarbAmount = 0
        currentSodiumAmount = 0
        currentWaterAmount = 0
        currentPhosphorusAmount = 0
        currentSugarAmount = 0

        for food in loggedFoods:
            if food.patient.username == loggedInUsername and food.date_time.date() == dt.today().date():
                # The foods here will be from the right user and will be today
                num_servings = food.quantity
                for nutrient in allNutrientInFoodData:
                    if nutrient.food.food_name == food.food.food_name:
                        if nutrient.nutrient.nutrient_name == "Protein":
                            currentProteinAmount += round(nutrient.amount * num_servings, 2)
                        elif nutrient.nutrient.nutrient_name == "Potassium, K":
                            currentPotassiumAmount += round(nutrient.amount * num_servings, 2)
                        elif nutrient.nutrient.nutrient_name == "Carbohydrate, by difference":
                            currentCarbAmount += round(nutrient.amount * num_servings, 2)
                        elif nutrient.nutrient.nutrient_name == "Sodium, Na":
                            currentSodiumAmount += round(nutrient.amount * num_servings, 2)
                        elif nutrient.nutrient.nutrient_name == "Water":
                            currentWaterAmount += round(nutrient.amount * num_servings, 2)
                        elif nutrient.nutrient.nutrient_name == "Phosphorus, P":
                            currentPhosphorusAmount += round(nutrient.amount * num_servings, 2)
                        elif nutrient.nutrient.nutrient_name == "Sugars, total including NLEA":
                            currentSugarAmount += round(nutrient.amount * num_servings, 2)

        # Recommended Amounts
        patientKG = patientData.weight * 0.453592
        proteinAmount = patientKG * 0.6

        for nutrient in nutrientData:
            if nutrient.nutrient_name == "Protein":
                currentAmount = round(currentProteinAmount, 2)
                recommendedAmount = round(proteinAmount, 0)
                recMeasurement = "G"
            elif nutrient.nutrient_name == "Potassium, K":
                currentAmount = round(currentPotassiumAmount, 2)
                recommendedAmount = 3000
                recMeasurement = "MG"
            elif nutrient.nutrient_name == "Carbohydrate, by difference":
                currentAmount = round(currentCarbAmount, 2)
                recommendedAmount = 250
                recMeasurement = "G"
            elif nutrient.nutrient_name == "Sodium, Na":
                currentAmount = round(currentSodiumAmount, 2)
                recommendedAmount = 2300
                recMeasurement = "MG"
            elif nutrient.nutrient_name == "Water":
                currentAmount = round(currentWaterAmount, 2)
                recommendedAmount = 3700
                recMeasurement = "MG"
            elif nutrient.nutrient_name == "Phosphorus, P":
                currentAmount = round(currentPhosphorusAmount, 2)
                recommendedAmount = 1500
                recMeasurement = "MG"
            elif nutrient.nutrient_name == "Sugars, total including NLEA":
                currentAmount = round(currentSugarAmount, 2)
                recommendedAmount = 30
                recMeasurement = "G"
            # Each nutrient needs a new object
            nutrient_object = {
                'nutrient' : nutrient,
                'currentAmount' : currentAmount,
                'dailyAmount' : recommendedAmount,
                'measurement' : recMeasurement
            }
            nutrients.append(nutrient_object)




        # Food Suggestions
        # Step 1: Find the two nutrients that are closest to going over
        #         the recommended amount
        nutriMax = 0
        nutriMaxName = ""
        nutri2Max = 0
        nutri2MaxName = ""
        
        for a_nutrient in nutrients :
            
            nutrient_level = a_nutrient['currentAmount'] / a_nutrient['dailyAmount']

            if nutrient_level > nutriMax:
                nutri2Max = nutriMax
                nutri2MaxName = nutriMaxName
                nutriMax = nutrient_level
                nutriMaxName = a_nutrient
            elif nutriMax > nutrient_level > nutri2Max:
                nutri2Max = nutrient_level
                nutri2MaxName = a_nutrient

        
        if nutriMax == 0 and nutri2Max == 0 :
            # print(favoriteFoods)
            # suggested_food_one = 
            # suggested_food_two = #random
            desc_one = "From your favorites"
            desc_two = "From your favorites"

        # Print them out to see if it worked
        # print(nutriMaxName['nutrient'])
        # print (round((nutriMax),4))
        # print(nutri2MaxName['nutrient'])
        # print (round((nutri2Max),4))

        # Step 2: Find which favorite food has the lowest in max nutrient 1
        #         Find which favorite food has the lowest in max nutrient 2
        favoriteFoods = Patient_Favorite_Food.objects.all()
        for favoriteFood in favoriteFoods :
            if favoriteFood.patient.id == loggedInPatientId :
                for nutrient in allNutrientInFoodData:
                    if nutrient.food.food_name == favoriteFood.food.food_name:
                        pass
                        # print(nutrient.nutrient.nutrient_name)
                        # print(nutrient.amount)
                        # nutrient_info = Nutrient_In_Food.objects.all()
                        # print(allNutrientInFoodData)

        # suggested_foods = {}

        context = {
            'data' : allNutrientInFoodData,
            'patientData' : patientData,
            'nutrients' : nutrients,
        }

    if loggedIn:
        return render(request,'homepages/index.html', context)
    else:
        return LandingPageView(request)

def SignOutPageView(request):
    global loggedIn
    global loggedInPatientId
    loggedIn = False
    loggedInPatientId = None
    return LandingPageView(request)

def AlertsPageView(request):
    global loggedInUsername
    
    if loggedIn:
        data = Alert.objects.all()
        user_alerts = []
        for alert in data:
            if alert.patient.username == loggedInUsername:
                user_alerts.append(alert)
                a = Alert.objects.get(id=alert.id)
                a.unread = False  # change field
                a.save() # this will update only
        
        context = {
            "alerts": user_alerts,
        }

        return render(request,'homepages/alerts.html', context)
    else:
        return LandingPageView(request)
    

def DiaryPageView(request):

    if loggedIn:
        food_data = Patient_Logs_Food.objects.all()
        nutrient_data = Nutrient_In_Food.objects.all()

        user_today_foods = []
        user_past_foods = []

        for food in food_data:
            if food.patient.username == loggedInUsername:
                food_object = {
                    'food': food,
                    'nutrients' : []
                }
                # Nutrients
                nutrient_list = []
                num_servings = food.quantity
                for nutrient in nutrient_data:
                    if nutrient.food.food_name == food.food.food_name:
                        nutrient_object = {
                            'name': nutrient.nutrient.nutrient_name,
                            'amount': round(nutrient.amount * num_servings, 2),
                            'measurement': nutrient.measurement.description
                        }
                        nutrient_list.append(nutrient_object)

                food_object['nutrients'] = nutrient_list

                if food.date_time.date() == dt.today().date():
                    user_today_foods.append(food_object)
                else:
                    user_past_foods.append(food_object)

        context = {
            "today_foods" : user_today_foods,
            "past_foods" : user_past_foods,
        }

        return render(request,'homepages/diary.html', context)
    else:
        return LandingPageView(request)

def AccountPageView(request, method):
    
    if loggedInPatientId != None:
        if request.method == 'POST' and method == "editPatientForm":
            patient_id = loggedInPatientId

            patient = Patient.objects.get(id = patient_id)

            patient.first_name = request.POST['first_name']
            patient.last_name = request.POST['last_name']
            patient.age = request.POST['age']
            patient.weight = request.POST['weight']
            patient.height = request.POST['height']
            patient.email = request.POST['email']
            patient.phone = request.POST['phone']

            patient.save()

            if request.POST['High Blood Pressure'] == "Yes":
                condition = Condition.objects.get(description="High Blood Pressure")
                patient_condition = Patient_Condition.objects.get(patient_id=loggedInPatientId, condition_id=condition.id)
                Patient_Condition.objects.create(patient_id=patientId.id, condition_id=condition.id)
                
                
            
            if request.POST['Diabetes'] == "Yes":

                condition = Condition.objects.get(description="Diabetes")
                patientId = Patient.objects.get(id=patient.id)
                Patient_Condition.objects.create(patient_id=patientId.id, condition_id=condition.id)


            return AccountPageView(request, "homeAccount")
        elif request.method == 'POST' and method == "changeUandPForm":
            patient_id = loggedInPatientId

            patient = Patient.objects.get(id = patient_id)

            patient.username = request.POST['username']
            patient.password = request.POST['password']

            patient.save()

            return AccountPageView(request, "homeAccount")
        else:     
            patientData = Patient.objects.get(id = loggedInPatientId)
            patientConditions = Patient_Condition.objects.all()
            loggedInPatientConditions = []

            for patient in patientConditions:
                if patient.patient_id == loggedInPatientId:
                    loggedInPatientConditions.append(Condition.objects.get(id = patient.condition_id))

            condition_data = Condition.objects.all()


            if method == "homeAccount":
                context = {
                    'patientData' : patientData,
                    'display': "homeAccount",
                    'conditions' : loggedInPatientConditions,
                    'condition_data' : condition_data,
                }
            elif method == "editPatient":
                context = {
                    'patientData' : patientData,
                    'display': "editPatient",
                    'conditions' : loggedInPatientConditions,
                    'condition_data' : condition_data,
                }
            else:
                context = {
                    'patientData' : patientData,
                    'display': "changeLoginInfo",
                    'conditions' : loggedInPatientConditions,
                    'condition_data' : condition_data,
                }
    if loggedIn:
        return render(request,'homepages/account.html', context)
    else:
        return LandingPageView(request)

def LandingPageView(request):
    global loggedIn
    if not loggedIn:
        context = {
            "signedIn": False
        }
    else:
        context = {
            "signedIn": True
        }
    return render(request,'homepages/landingpage.html', context)


def LoginPageView(request, method):
    global loggedIn
    global loggedInPatientId
    global loggedInUsername
    errors = []
    errors.clear()
    if request.method == 'POST' and method == "form":
        email = request.POST['email']
        username = request.POST['username']

        data = Patient.objects.all()

        for patient in data:
            if email == patient.email:
                errors.append("This email has already been registered") 
            if username == patient.username:
                errors.append("This username is already taken")
        
        condition_data = Condition.objects.all()

        if len(errors) != 0:
            context = {
                    "display" : "create",
                    "errors" : errors,
                    "condition_data": condition_data,
                }
            return render(request, 'homepages/login.html', context)
        else:
            patient = Patient()

            patient.first_name = request.POST['first_name']
            patient.last_name = request.POST['last_name']
            patient.username = request.POST['username']
            patient.password = request.POST['password']
            patient.age = request.POST['age']
            patient.weight = request.POST['weight']
            patient.height = request.POST['height']
            patient.email = request.POST['email']
            patient.phone = request.POST['phone']

            patient.save()

            if request.POST['High Blood Pressure'] == "Yes":

                condition = Condition.objects.get(description="High Blood Pressure")
                patientId = Patient.objects.get(id=patient.id)
                Patient_Condition.objects.create(patient_id=patientId.id, condition_id=condition.id)
                
                
            
            if request.POST['Diabetes'] == "Yes":

                condition = Condition.objects.get(description="Diabetes")
                patientId = Patient.objects.get(id=patient.id)
                Patient_Condition.objects.create(patient_id=patientId.id, condition_id=condition.id)

            

            loggedIn = True
            loggedInPatientId = patient.id
            loggedInUsername = patient.username
            
            return indexPageView(request)

    elif request.method == 'POST' and method == "loginform":
        
        username = request.POST['username']
        password = request.POST['password']
        notFound = False

        data = Patient.objects.all()

        for patient in data:
            if username == patient.username and password == patient.password:
                loggedIn = True
                loggedInPatientId = patient.id
                loggedInUsername = patient.username
                return indexPageView(request)
            else :
                notFound = True
            
        if notFound:
            context = {
                "display" : "login",
                "errors" : "The username or password are incorrect"
            }
            return render(request, 'homepages/login.html', context)
    else:

        if (method == "landing" or method == "create" or method == "login") and loggedIn:
            return indexPageView(request)
        elif method == "landing" :
            context = {
                "display" : "original"
            }
        elif method == "create":

            condition_data = Condition.objects.all()

            context = {
                "display" : "create",
                "condition_data": condition_data,
            }
        else :
            context = {
                "display" : "login",
                "errors" : ""
            }

        return render(request, 'homepages/login.html', context)

def AboutPageView(request):
    global loggedIn
    patientConditions = Patient_Condition.objects.all()
    loggedInPatientConditions = []

    for patient in patientConditions:
        if patient.patient_id == loggedInPatientId:
            condition_obj = Condition.objects.get(id = patient.condition_id)
            loggedInPatientConditions.append(condition_obj.description)

    if not loggedIn:
        context = {
            "signedIn": False
        }
    else:
        context = {
            "signedIn": True,
            "conditions": loggedInPatientConditions,
        }

    return render(request, 'homepages/about.html', context)
# def apiPageView(request) :
#     response=requests.get(f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={settings.API_KEY}&query=Cheddar%20Cheese').json()
#     print(response)
#     return render(request,'homepages/apitest.html',{'response':response})


def apiJSONView(request) :
    response=requests.get(f'https://api.nal.usda.gov/fdc/v1/foods/search?query=burger&dataType=&pageSize=1&pageNumber=1&sortBy=dataType.keyword&sortOrder=asc&api_key={settings.API_KEY}').json()
    return JsonResponse(response)


def LogFoodPageView(request) :
    food_names = {}
    current_date = dt.now().date()
    formatted_date = f'{current_date.strftime("%b")} {current_date.strftime("%d")}, {current_date.strftime("%Y")}'

    if 'name' in request.GET:
        name = request.GET['name']
        response=requests.get(f'https://api.nal.usda.gov/fdc/v1/foods/search?query={name}&dataType=&pageSize=8&pageNumber=1&sortBy=dataType.keyword&sortOrder=desc&api_key={settings.API_KEY}')
        data = response.json()
        searchedFoods = data['foods']
 
        for idx, food in enumerate(searchedFoods) :
            food_names['food_name' + str(idx+1)] = food['description']
    

    if request.method == "POST":
        post_form_data = request.POST
        print(post_form_data['food_names_options'])
        print(post_form_data['numServings'])
        print(post_form_data['dateTime'])

        all_form_data = {}
        searched_food = {}
        searched_food_data = {}
        food_nutrients = {}
        food_found = False

        nutrientList = [
            'Protein',
            'Potassium, K',
            'Carbohydrate, by difference',
            'Sodium, Na',
            'Water',
            'Phosphorus, P',
            'Sugars, total including NLEA',
        ]

        # get the name of the food they typed in and send it call the api with it!
        name = f"{post_form_data['food_names_options']}"
        response=requests.get(f'https://api.nal.usda.gov/fdc/v1/foods/search?query={name}&dataType=&pageSize=1&pageNumber=1&sortBy=dataType.keyword&sortOrder=desc&api_key={settings.API_KEY}')
        # turn it into json to be able to deal with the info we get
        data = response.json()
        # keep just the info about the specific FOOD and from only the FIRST one returned
        searched_food = data['foods'][0]

        # the database food table accessible to us in a for loop
        food_table = Food.objects.all()
        
        # the database nutrient table accessible to us in list (if/in)
        nutrient_table = []
        for a_nutrient in Nutrient.objects.all() :
            # print(a_nutrient)
            nutrient_table.append(f'{a_nutrient}')

        # the database nutrient_in_food table accessible to us in list (if/in)
        nutrient_in_food_table = []
        for a_nutrient_in_food in Nutrient_In_Food.objects.all() :
            # print(a_nutrient_in_food)
            nutrient_in_food_table.append(f'{a_nutrient_in_food}')

        # the database measurement table accessible to us in list (if/in)
        measurement_table = []
        for a_measurement in Measurement.objects.all() :
            # print(a_measurement)
            measurement_table.append(f'{a_measurement}')


        # checking the database for the inputed food
        food_found = False
        for a_food in food_table :
            if searched_food['description'] == a_food.food_name :
                food_found = True

        # load it up to be ready to save in the database if it's not found!
        if not food_found: 
            food_data = Food(
                food_name = searched_food['description'],
            )
            # send it over to the database!
            food_data.save()
            

        # get all the nutrients from the searched foods and check if it's 
        # nutrients that we care about
        for nutrient in searched_food['foodNutrients'] :
            if nutrient['nutrientName'] in nutrientList:
                food_nutrients[ nutrient['nutrientName'] ] = [{ 'value' : nutrient['value']}, {'unitName' : nutrient['unitName']}]
                # if they are not already in the database, load it up and send it over!

                if not nutrient['unitName'] in measurement_table:
                    measurement_data = Measurement(
                        description = nutrient['unitName'],
                    )
                    measurement_data.save()
                    # adding the new things to our list - may be unneccessary...
                    measurement_table.append(nutrient['unitName'])

                if not nutrient['nutrientName'] in nutrient_table:
                    nutrient_data = Nutrient(
                        # this will have some logic to decide if macro or micro
                        # alsooo it doesn't like it?
                        nutrient_name = nutrient['nutrientName'],
                    )
                    nutrient_data.save()
                    # adding the new things to our list - may be unneccessary...
                    nutrient_table.append(nutrient['nutrientName'])
                    

                # check if the food/nutrient combination has already been recorded in the database
                # if not, load it up and send it over!
                if not f"{searched_food['description']}: {nutrient['nutrientName']}" in nutrient_in_food_table :
                    nutrient_in_food_data = Nutrient_In_Food(
                        nutrient = Nutrient.objects.get(nutrient_name= nutrient['nutrientName']),
                        food = Food.objects.get(food_name= searched_food['description']),
                        measurement = Measurement.objects.get(description= nutrient['unitName']),
                        amount = nutrient['value'],
                    )
                    nutrient_in_food_data.save()
                    # adding the new things to our list - may be unneccessary...
                    nutrient_in_food_table.append(f"{searched_food['description']}: {nutrient['nutrientName']}")

        patient_logs_food_data = Patient_Logs_Food(
            food = Food.objects.get(food_name= searched_food['description']),
            patient = Patient.objects.get(username= loggedInUsername),
            measurement = Measurement.objects.get(description= "Servings"),
            quantity = post_form_data['numServings'],
            date_time = post_form_data['dateTime'],
        )
        patient_logs_food_data.save()

        # thought i would need this data but didn't
        # searched_food_form_data = Food.objects.all()
        # measurement_form_data = Measurement.objects.all()
        # nutrient_form_data = Nutrient.objects.all()
        # nutrient_in_food_form_data = Nutrient_In_Food.objects.all()


        # all_form_data = {
        #     'food' : searched_food_form_data,
        #     'measurement' : measurement_form_data,
        #     'nutrient' : nutrient_form_data,
        #     'nutrient_in_food' : nutrient_in_food_form_data
        # }


        # Create alerts
        allNutrientInFoodData = Nutrient_In_Food.objects.all()
        loggedFoods = Patient_Logs_Food.objects.all()
        patientData = Patient.objects.get(id = loggedInPatientId)

        currentProteinAmount = 0
        currentPotassiumAmount = 0
        currentCarbAmount = 0
        currentSodiumAmount = 0
        currentWaterAmount = 0
        currentPhosphorusAmount = 0
        currentSugarAmount = 0

        for food in loggedFoods:
            if food.patient.username == loggedInUsername and food.date_time.date() == dt.today().date():
                num_servings = food.quantity
                for nutrient in allNutrientInFoodData:
                    if nutrient.food.food_name == food.food.food_name:
                        if nutrient.nutrient.nutrient_name == "Protein":
                            currentProteinAmount += round(nutrient.amount * num_servings, 2)
                        elif nutrient.nutrient.nutrient_name == "Potassium, K":
                            currentPotassiumAmount += round(nutrient.amount * num_servings, 2)
                        elif nutrient.nutrient.nutrient_name == "Carbohydrate, by difference":
                            currentCarbAmount += round(nutrient.amount * num_servings, 2)
                        elif nutrient.nutrient.nutrient_name == "Sodium, Na":
                            currentSodiumAmount += round(nutrient.amount * num_servings, 2)
                        elif nutrient.nutrient.nutrient_name == "Water":
                            currentWaterAmount += round(nutrient.amount * num_servings, 2)
                        elif nutrient.nutrient.nutrient_name == "Phosphorus, P":
                            currentPhosphorusAmount += round(nutrient.amount * num_servings, 2)
                        elif nutrient.nutrient.nutrient_name == "Sugars, total including NLEA":
                            currentSugarAmount += round(nutrient.amount * num_servings, 2)

        patientKG = patientData.weight * 0.453592
        proteinAmount = patientKG * 0.6

        """
        # Recommended Daily Amounts:
        Protein                         0.6 g / kg
        Potassium, K                    3000 mg
        Carbohydrate, by difference     250 g
        Sodium, Na                      2300 mg
        Water                           3700 mg
        Phosphorus, P                   3500 mg
        Sugar                           30 g
        """

        if currentProteinAmount > proteinAmount:
            alert_name = "High Protein Levels"
            allAlertTypes = Alert_Type.objects.all()
            alert_type_names = []
            for alert_type in allAlertTypes:
                alert_type_names.append(alert_type.name)
            if alert_name not in alert_type_names:
                alert_type_object = Alert_Type(
                    name = alert_name,
                    description = "Your protein levels exceed the recommended amount"
                )
                alert_type_object.save()

            alert_object = Alert(
                date_time = dt.now(),
                unread = True,
                alert_type = Alert_Type.objects.get(name = alert_name),
                patient = Patient.objects.get(id = loggedInPatientId)
            )
            alert_object.save()

        if currentPotassiumAmount > 3000:
            alert_name = "High Potassium Levels"
            allAlertTypes = Alert_Type.objects.all()
            alert_type_names = []
            for alert_type in allAlertTypes:
                alert_type_names.append(alert_type.name)
            if alert_name not in alert_type_names:
                alert_type_object = Alert_Type(
                    name = alert_name,
                    description = "Your potassium levels exceed the recommended amount"
                )
                alert_type_object.save()

            alert_object = Alert(
                date_time = dt.now(),
                unread = True,
                alert_type = Alert_Type.objects.get(name = alert_name),
                patient = Patient.objects.get(id = loggedInPatientId)
            )
            alert_object.save()

        if currentCarbAmount > 250:
            alert_name = "High Carb Levels"
            allAlertTypes = Alert_Type.objects.all()
            alert_type_names = []
            for alert_type in allAlertTypes:
                alert_type_names.append(alert_type.name)
            if alert_name not in alert_type_names:
                alert_type_object = Alert_Type(
                    name = alert_name,
                    description = "Your carbohydrate levels exceed the recommended amount"
                )
                alert_type_object.save()

            alert_object = Alert(
                date_time = dt.now(),
                unread = True,
                alert_type = Alert_Type.objects.get(name = alert_name),
                patient = Patient.objects.get(id = loggedInPatientId)
            )
            alert_object.save()

        if currentSodiumAmount > 2300:
            alert_name = "High Sodium Levels"
            allAlertTypes = Alert_Type.objects.all()
            alert_type_names = []
            for alert_type in allAlertTypes:
                alert_type_names.append(alert_type.name)
            if alert_name not in alert_type_names:
                alert_type_object = Alert_Type(
                    name = alert_name,
                    description = "Your sodium levels exceed the recommended amount"
                )
                alert_type_object.save()

            alert_object = Alert(
                date_time = dt.now(),
                unread = True,
                alert_type = Alert_Type.objects.get(name = alert_name),
                patient = Patient.objects.get(id = loggedInPatientId)
            )
            alert_object.save()

        if currentWaterAmount > 3700:
            alert_name = "High Water Levels"
            allAlertTypes = Alert_Type.objects.all()
            alert_type_names = []
            for alert_type in allAlertTypes:
                alert_type_names.append(alert_type.name)
            if alert_name not in alert_type_names:
                alert_type_object = Alert_Type(
                    name = alert_name,
                    description = "Your water levels exceed the recommended amount"
                )
                alert_type_object.save()

            alert_object = Alert(
                date_time = dt.now(),
                unread = True,
                alert_type = Alert_Type.objects.get(name = alert_name),
                patient = Patient.objects.get(id = loggedInPatientId)
            )
            alert_object.save()

        if currentPhosphorusAmount > 3500:
            alert_name = "High Phosphorus Levels"
            allAlertTypes = Alert_Type.objects.all()
            alert_type_names = []
            for alert_type in allAlertTypes:
                alert_type_names.append(alert_type.name)
            if alert_name not in alert_type_names:
                alert_type_object = Alert_Type(
                    name = alert_name,
                    description = "Your phosphorus levels exceed the recommended amount"
                )
                alert_type_object.save()

            alert_object = Alert(
                date_time = dt.now(),
                unread = True,
                alert_type = Alert_Type.objects.get(name = alert_name),
                patient = Patient.objects.get(id = loggedInPatientId)
            )
            alert_object.save()

        if currentSugarAmount > 30:
            alert_name = "High Sugar Levels"
            allAlertTypes = Alert_Type.objects.all()
            alert_type_names = []
            for alert_type in allAlertTypes:
                alert_type_names.append(alert_type.name)
            if alert_name not in alert_type_names:
                alert_type_object = Alert_Type(
                    name = alert_name,
                    description = "Your sugar levels exceed the recommended amount"
                )
                alert_type_object.save()

            alert_object = Alert(
                date_time = dt.now(),
                unread = True,
                alert_type = Alert_Type.objects.get(name = alert_name),
                patient = Patient.objects.get(id = loggedInPatientId)
            )
            alert_object.save()

    return render (request, 'homepages/logfood.html', { "food_names": 
    food_names} )



def PickFavoritesPageView(request):
    food_list = [
        'Fruit juice blend, 100% juice', #1,1
        'Blueberries, raw', #1,2
        'Apple, raw', #1,3
        'Banana nectar', #1,4
        'Cake, sponge', #1,5
        'Blueberries, dried', #1,6
        'Blueberries, dried', #1,7
        'Blueberries, dried', #1,8
        'Blueberries, dried', #1,9
        'Blueberries, dried',
        'Blueberries, dried',
        'Blueberries, dried',
        'Blueberries, dried',
        'Blueberries, dried',
        'Blueberries, dried'
    ]

    if request.method == 'POST':
        favfoods = request.POST.getlist('foods')
        print(favfoods)

        for favfood in favfoods :
            print(favfood)
            response=requests.get(f'https://api.nal.usda.gov/fdc/v1/foods/search?query={favfood}&dataType=&pageSize=1&pageNumber=1&sortBy=dataType.keyword&sortOrder=desc&api_key={settings.API_KEY}')
            # turn it into json to be able to deal with the info we get
            data = response.json()
            # keep just the info about the specific FOOD and from only the FIRST one returned
            clicked_food = data['foods'][0]


            food_table = Food.objects.all()

            # checking the database for the inputed food
            food_found = False
            for a_food in food_table :
                if clicked_food['description'] == a_food.food_name :
                    food_found = True

            # load it up to be ready to save in the database if it's not found!
            if not food_found: 
                food_data = Food(
                    food_name = clicked_food['description'],
                )
                # send it over to the database!
                food_data.save()

            # THIS IS FOR MAKING PATIENT FAVORITE FOOD NOT DUPLICATABLE
            #  BUT IT DO NOT BE WORKING I need to figure out how to access the current user and put the firstname into a string to check if it's already there
            # patient_favorite_food_table = Patient.objects.all()
            # for a_patient_favorite_food in patient_favorite_food_table :
            #     if a_patient_favorite_food.patient.id == loggedInPatientId :
            #         print(f'{a_patient_favorite_food.patient.first_name}: {a_patient_favorite_food}')
            #         patient_favorite_food_table.append(f'{a_patient_favorite_food}')

            patient_favorite_food_data = Patient_Favorite_Food(
                patient = Patient.objects.get(username= loggedInUsername),
                food = Food.objects.get(food_name= clicked_food['description']),
                is_favorite = True
            )

            patient_favorite_food_data.save()


    context = {
        'food_list' : food_list
    }
    

    return render(request, 'homepages/pickfavorites.html', context)

def getUsername():
    global loggedInUsername
    return loggedInUsername
