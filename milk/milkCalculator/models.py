from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class MilkData(models.Model):
    issue_date = models.DateField()
    qty = models.FloatField()
    total_qty = models.IntegerField(null=True)
    price = models.IntegerField(null=True)


class MilkView(models.Model):
    id = models.BigIntegerField(primary_key=True)
    issue_date = models.DateField()
    qty = models.IntegerField()
    price = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'milk_view'



class Months(models.Model):
    name = models.CharField(max_length=15)
                
    def __str__(self):
        return self.name
    



class UserProfileInfo(models.Model):

    # Create relationship (don't inherit from User!)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Add any additional attributes you want
    # pip install pillow to use this!
    # Optional: pip install pillow --global-option="build_ext" --global-option="--disable-jpeg"
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.user.username