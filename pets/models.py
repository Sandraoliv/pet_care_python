from django.db import models
from groups.models import Group
from traits.models import Trait


class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    SEX_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Not Informed", "Not Informed"),
    ]
    sex = models.CharField(max_length=20, choices=SEX_CHOICES, default="Not Informed")
    group = models.ForeignKey("groups.Group", on_delete=models.PROTECT, related_name="pets")
    traits = models.ManyToManyField("traits.Trait", related_name="pets")

    def __str__(self):
        return self.name
