from django.db import models
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator

def validate_text(text):
  if len(text)== 0:
    print(len(text))
    raise ValidationError("Please enter a value")

class Details(models.Model):
  name = models.CharField(max_length=60,validators=[MinLengthValidator(5)])
  description = models.TextField()
  location = models.CharField(max_length=60)
  date = models.DateField()
  image=models.ImageField()
  id = models.AutoField(primary_key=True)

  def __str__(self):
    return self.name+str(self.id)
    # Create your models here.
