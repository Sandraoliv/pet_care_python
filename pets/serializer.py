from rest_framework import serializers
from .models import SEX_CHOICES
from traits import TraitSerializer
from groups import GroupSerializer


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weigth = serializers.FloatField()
    sex = serializers.ChoiceField(choices=SEX_CHOICES.choices, default=SEX_CHOICES.NOT_INFORMED)
    group = GroupSerializer(read_only=True)
    traits = TraitSerializer(many=True, read_only=True)



