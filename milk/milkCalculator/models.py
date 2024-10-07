from django.db import models

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