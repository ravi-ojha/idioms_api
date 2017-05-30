# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import json

from django.db import models


class Idiom(models.Model):
    """
    Model to store the idiom, proverb or phrase
    """

    # The idiom we are talking about
    title = models.CharField(max_length=512, null=True)

    # Meaning of the idiom
    meaning = models.TextField(null=True)

    # List of examples for the usage of this idiom
    examples = models.TextField(null=True)

    def set_examples(self, eg):
        self.examples = json.dumps(eg)

    def get_examples(self):
        return json.loads(self.examples)

    class Meta:
        verbose_name = "Idiom"
        verbose_name_plural = "Idioms"

    def __str__(self):
        return self.title

    @staticmethod
    def get_random_idiom():
        # Get the count of total idioms present in db
        count = Idiom.objects.all().count()

        # Get a random number within the range of total idioms
        idx = random.randrange(count)

        # Get all the idiom objects as queryset
        idioms = Idiom.objects.all()

        # Return the one with index value corresponding to idx
        return idioms[idx]


class IdiomOfTheDay(models.Model):
    """
    Model to store which idiom was shown on which day
    """
    date = models.DateField()
    idiom = models.ForeignKey(Idiom, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Idiom of the Day"
        verbose_name_plural = "Idiom of the Day"
