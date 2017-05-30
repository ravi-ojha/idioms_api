# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import simplejson

from django.core.cache import cache
from django.http import HttpResponse


from idioms.models import Idiom, IdiomOfTheDay

# Create your views here.

def get_idiom_of_the_day(request, curr_date):
    """
    Arg:
        request - Django request object
        curr_date (unicode string) - date string in the format DD-MM-YYYY

    Returns:
        dict
    """

    # Try to get from cache
    key = "iod-%s" % curr_date
    idiom = cache.get(key)

    if idiom is None:
        # Create the python datetime object from date string
        datetime_obj = datetime.datetime.strptime(curr_date, '%d-%m-%Y')
        date_obj = datetime_obj.date()

        # Query for the date obj in IdiomOfTheDay model
        idiom_of_the_day = IdiomOfTheDay.objects.filter(date=date_obj)

        # If there exists an entry for the day, then get that
        # Else create one right away
        if idiom_of_the_day:
            idiom_of_the_day = idiom_of_the_day[0]
            # Get the idiom which is a FK to idiom_of_the_day object
            idiom = idiom_of_the_day.idiom
        else:
            # Get a random idiom out of the list of idioms from Idiom model
            idiom = Idiom.get_random_idiom()
            IdiomOfTheDay.objects.create(date=date_obj, idiom=idiom)

        # Cache for 48 hours
        cache.set(key, idiom, 60*60*48)

    return_dict = {
        'title': idiom.title,
        'meaning': idiom.meaning,
        'examples': idiom.get_examples(),
    }

    data = simplejson.dumps(return_dict)
    return HttpResponse(data, content_type='application/json')
