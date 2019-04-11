from django.db import models
 
# Create your models here.

class Post(models.Model):
    company_name=models.CharField(max_length=100, verbose_name="Company name")
    description = models.TextField(verbose_name="Description")
    workloc=models.CharField(max_length=100, verbose_name="Work location")
    start_date = models.DateTimeField(verbose_name="Start date")
    completition_date = models.DateTimeField(verbose_name="completion date")
    post_expiry_date = models.DateTimeField(verbose_name="Post expiry date")
    appicantno = models.IntegerField(default=0, blank=True, null=True)
    competition_type= models.TextField(verbose_name="Competition type")
    workdescription = models.TextField(verbose_name="Work Description")
    stipend = models.FloatField(blank=True, null=True, default=0)
    reqskill=models.TextField(verbose_name="Required skill Set")
    product_detail=models.TextField(verbose_name="product detail")

def __str__(self):
        return self.company_name       

