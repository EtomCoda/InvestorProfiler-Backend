from django.db import models
from core.models import RiskProfile

# Create your models here.


class FundCategory(models.Model):
    name = models.CharField(max_length=100)
    percent = models.DecimalField(decimal_places=2, max_digits=5)  
    risk_profile = models.ForeignKey(RiskProfile, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return f"{self.name} ({self.percent})"

class Fund(models.Model):
    name = models.CharField(max_length=100, unique=True)
    categories = models.ManyToManyField(FundCategory, related_name='funds')
    score = models.DecimalField(decimal_places=2, max_digits=5, null=True, blank=True)

    def excess_return(self):
        return self.one_year_return - self.risk_free_rate_history

    def __str__(self):
        return self.name
    

# MODEL FOR FUND DATA TO CALCULATE RANKING- NOT MIGRATED YET
# NEED DATA TO POPULATE THESE PARTS 
#     
# class FundReturn(models.Model):
#     fund = models.ForeignKey(Fund, on_delete=models.CASCADE, related_name='returns')
#     inception_date = models.DateField(null=True, blank=True)
#     one_year_return = models.DecimalField(decimal_places=4, max_digits=10, null=True, blank=True)  # annualized return
#     total_return = models.DecimalField(max_digits=6, decimal_places=2)
#     risk_free_rate = models.DecimalField(max_digits=5, decimal_places=2)
#     star_rating_3yr = models.IntegerField(null=True, blank=True)
#     star_rating_5yr = models.IntegerField(null=True, blank=True)
#     star_rating_10yr = models.IntegerField(null=True, blank=True)

# COMMENTED BECAUSE DATA MAY BE GOTTEN FROM CSV SHEET MIGHT NOT NEED TO STORE IN DB YET