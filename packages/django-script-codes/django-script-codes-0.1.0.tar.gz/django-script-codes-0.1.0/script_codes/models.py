# -*- coding: utf-8 -*-

from django.core.validators import MaxValueValidator
from django.db import models
from model_utils.models import TimeStampedModel


class Script(TimeStampedModel):
    code = models.CharField(max_length=4, unique=True)
    number = models.PositiveSmallIntegerField(
        unique=True, validators=[MaxValueValidator(999)])
    name = models.CharField(max_length=64)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return '{}, {}, {}'.format(self.code, self.number, self.name)
