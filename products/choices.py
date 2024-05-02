from django.db import models


class CategoryTypeChoices(models.IntegerChoices):
    GENERAL = 1, "General"
    HOUSEHOLD = 2, "Household"
    OUTDOOR = 3, "Outdoor"


