from .models import StatsResumed, Dataset
import pandas as pd

def getCredentials(user, function):
    def Decorator(*args, **kwargs):
        if user.organisation is None:
            return "you don't have permission to do that, contact you company to unlock the resource"
        elif not user.organisation.isHubMember:
            return function(True, user)
        else:
            return function(False, user)
    return Decorator

def showMaps(limited, user):
    if limited:
        return Dataset.objects.get(organisation_id = user.organisation_id).filename
    else:
        x =  Dataset.objects.get(organisation_id = user.organisation_id).filename
        df = pd.read_csv(x.path)

        return df.columns
        

def showStats(limited, user):
    if limited:
        return  'Functionality reduced - Funding Partner'
    else:
        obj = list(StatsResumed.objects.filter(id=1).values())
        for row in obj:
            return row


def showCharts(limited,user):
    if limited:
        return 'Functionality reduced - Funding Partner'
    else:
        return 'Unlimited power! - Hub Manager' 








