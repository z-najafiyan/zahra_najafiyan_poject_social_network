from math import floor

from django.db import models
from django.utils.timezone import now


class PostManege(models.Manager):
    def life_time(self, time):
        lifetime = (now() - time).total_seconds()
        print("l",lifetime)

        hour = lifetime / 3600
        print("h",hour)
        if hour < 1:
            return 'A little while ago'
        if hour < 24:
            return "hour"+str(floor(lifetime / 3600))
        month = lifetime / 2628000
        print('month',month)
        if month < 1:
            return "days"+str(floor(lifetime / 86400))
        year = lifetime / 31536000
        print("yer",year)
        if year < 1:
            return 'month'+str(floor(lifetime / 2628000))
        if year > 1:
            return "year"+str(floor(lifetime / 31536000))
