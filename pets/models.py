from django.db import models
from groups.models import Group
from traits.models import Trait


class SEX_CHOICES(models.TextChoices):
    MALE = ("Male",)
    FEMALE = ("Female",)
    NOT_INFORMED = "Not Informed"


class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(max_length=20, choices=SEX_CHOICES.choices, default=SEX_CHOICES.NOT_INFORMED)
       
    group = models.ForeignKey(
        "groups.Group", on_delete=models.PROTECT, related_name="pets"
    )
    traits = models.ManyToManyField("traits.Trait", related_name="pets")

   
