# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import simplejson

from django.core.cache import cache
from django.http import HttpResponse


from idioms.models import Idiom, IdiomOfTheDay

# Create your views here.

past_idiom_data = {
    'title': 'dwell in the past',
    'meaning': 'to react to conditions that existed long ago rather than those that exist now.',
    'examples': ["You should stop dwelling in the past and embrace the current situation and plan for the future. For example: Correct the system date to the present date, you're living in the past."],
}

future_idiom_data = {
    'title': 'see what the future has in store',
    'meaning': 'try to find or wander about what would come in the future.',
    'examples': ["It seems you're living too far in the future. Don't try to see this chrome extension's future store."],
}


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

        # Get system date
        sys_date = datetime.datetime.now()
        sys_date = sys_date.date()

        # Find difference
        td = sys_date - date_obj
        td_days = td.days

        # If days diff is more than 2 then show some
        # If difference is negative then user is in the future
        if td_days <= -2:
            data = simplejson.dumps(future_idiom_data)
            return HttpResponse(data, content_type='application/json')

        # If difference is positive then user is in the past
        if td_days >= 2:
            data = simplejson.dumps(past_idiom_data)
            return HttpResponse(data, content_type='application/json')

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
        cache.set(key, idiom, 60 * 60 * 48)

    return_dict = {
        'title': idiom.title,
        'meaning': idiom.meaning,
        'examples': idiom.get_examples(),
    }

    data = simplejson.dumps(return_dict)
    return HttpResponse(data, content_type='application/json')
