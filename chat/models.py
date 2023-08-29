from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid

# Create your models here.


   
   
class Person(models.Model):
   unique_id = models.CharField(max_length=250, unique=True)
   interests = models.CharField(max_length=50)
   on_chat = models.BooleanField(default=False)
   
   def __str__(self):
      return str(self.unique_id) + " " + "/" + " " + self.interests            




class PersonImage(models.Model):
   person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='images', verbose_name="Person")
   images = models.ImageField(upload_to='images/')
