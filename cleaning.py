import pandas as pd
RUNNING_COLS = ["Type d'activité", "Date", "Distance", "Calories", "Durée", "Fréquence cardiaque moyenne", "Fréquence cardiaque maximale",
                "Cadence de course moyenne", "Cadence de course maximale", "Allure moyenne", "Meilleure allure", "Longueur moyenne des foulées",
                "Temps de contact moyen avec le sol"]

SWIM_COLS = ["Type d'activité", "Date", "Distance", "Calories", "Durée", "Nombre total de mouvements", "SWOLF moyen", "Fréquence moy. des coups",
             "Temps de déplacement", "Nombre de circuits"]

CYCLING_COLS = ["Type d'activité", "Date", "Distance", "Calories", "Durée", "Fréquence cardiaque moyenne", "Fréquence cardiaque maximale",
                "Allure moyenne", "Meilleure allure"]


def rmv_coma(val):
    """Remove the coma, to change dtype to int64 """
    if "," in val:
        val = val.replace(",", "")
    return val


def coma_to_dot(val):
    """Change coma to dot, to change dtype to float """
    if "," in val:
        val = val.replace(",", ".")
    return val


def convert_duration(duration):
    a = [round(float(b)) for b in duration.split(":")]
    return a[0] * 60 + a[1] + a[2]/60


def convert_allure(allure):
    a = [round(float(b)) for b in allure.split(":")]
    return a[0] + a[1]/60


activities = pd.read_csv('../../Documents/Portfiolio (Python - BI)/Activities_all.csv')


differents_act = activities.groupby("Type d'activité").count()["Date"]

""" Change Date to datetime dtype """
activities["Date"] = pd.to_datetime(activities["Date"])

""" Change Durée in minutes """
activities["Durée"] = activities["Durée"].apply(convert_duration)

""" Remove coma in calories and then change to int64 """
activities["Calories"] = activities["Calories"].apply(rmv_coma).astype(int)

outdoor_activities = activities.query("Distance != '0.00' and Distance != '--'")

runs = outdoor_activities[outdoor_activities["Type d'activité"] == "Course à pied"][RUNNING_COLS]
swims = outdoor_activities[outdoor_activities["Type d'activité"] == "En piscine"][SWIM_COLS]
bikes = outdoor_activities[outdoor_activities["Type d'activité"] == "Cyclisme"][CYCLING_COLS]

""" Runs distances are in kilometers and allure is in min/km """
runs["Distance"] = runs["Distance"].astype(float)
runs["Allure moyenne"] = runs["Allure moyenne"].apply(convert_allure)
runs["Meilleure allure"] = runs["Meilleure allure"].apply(convert_allure)

""" Bikes distance is in kilometer """
bikes["Distance"] = bikes["Distance"].astype(float)
bikes["Allure moyenne"] = bikes["Allure moyenne"].astype(float)
bikes["Meilleure allure"] = bikes["Meilleure allure"].astype(float)

""" Swims distances are in meters """
swims["Distance"] = swims["Distance"].apply(rmv_coma).astype(int)
swims["Nombre total de mouvements"] = swims["Nombre total de mouvements"].astype(int)
swims["Temps de déplacement"] = swims["Temps de déplacement"].apply(convert_duration)

runs.to_csv('runs.csv', index=False)
bikes.to_csv('bikes.csv', index=False)
swims.to_csv('swims.csv', index=False)
