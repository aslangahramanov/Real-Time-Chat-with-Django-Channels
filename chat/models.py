from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid

# Create your models here.


   

class Interest(models.Model):
   title = models.CharField(max_length=100)
   
   
   def __str__(self):
      return str(self.title)


   
   
class Person(models.Model):
   unique_id = models.CharField(max_length=250, unique=True)
   interests = models.ManyToManyField(Interest)
   on_chat = models.BooleanField(default=False)
   
   def __str__(self):
      return str(self.unique_id)          




class PersonImage(models.Model):
   person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='images', verbose_name="Person")
   images = models.ImageField(upload_to='images/')
