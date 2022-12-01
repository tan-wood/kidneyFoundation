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

from homepages.views import getUsername

def date_processor(request):
    current_date = dt.now().date()
    formatted_date = f'{current_date.strftime("%b")} {current_date.strftime("%d")}, {current_date.strftime("%Y")}'

    return {
        'formatted_date' : formatted_date
    }

def message_processor(request):
    loggedInUsername = getUsername()
    print("LOGGED IN USERNAME: ")
    print(loggedInUsername)
    print("\n\n")
    allAlerts = Alert.objects.all()
    user_unread_alerts = []
    for alert in allAlerts:
        if alert.unread == True and alert.patient.username == loggedInUsername:
            user_unread_alerts.append(alert)

    return {
        'unread_messages' : len(user_unread_alerts)
    }