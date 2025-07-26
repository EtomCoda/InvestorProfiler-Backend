from django.urls import path
from .views import get_fund_profile



urlpatterns = [
    path('get-fund-profile/', get_fund_profile, name='get_fund_profile')
    ]
