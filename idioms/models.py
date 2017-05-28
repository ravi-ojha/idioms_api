# -*- coding: utf-8 -*-
from __future__ import unicode_literals


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

