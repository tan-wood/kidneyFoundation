# def message_processor(request):
#     if request.user.is_authenticated:
#         no_msgs = request.user.profile.msgs
#     else:
#         no_msgs = 0
#     return {
#         'messages' : no_msgs
#     }
from homepages.models import Alert
from datetime import datetime as dt
from datetime import timedelta

from homepages.views import getUsername

def date_processor(request):
    # print("Dt.now():")
    # print(dt.now())
    # print("Dt.now - timedelta 7 hours")
    # print(dt.now() - timedelta(hours=7))
    # print("Dt.now().date()")
    # print(dt.now().date())
    current_date = (dt.now() - timedelta(hours=7)).date()
    formatted_date = f'{current_date.strftime("%b")} {current_date.strftime("%d")}, {current_date.strftime("%Y")}'

    return {
        'formatted_date' : formatted_date
    }

def message_processor(request):
    loggedInUsername = getUsername()
    allAlerts = Alert.objects.all()
    user_unread_alerts = []
    for alert in allAlerts:
        if alert.unread == True and alert.patient.username == loggedInUsername:
            user_unread_alerts.append(alert)

    return {
        'unread_messages' : len(user_unread_alerts)
    }