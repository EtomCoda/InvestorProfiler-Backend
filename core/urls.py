from django.urls import path
from .views import get_risk_profile
# from .views import calculate
from .views import submit_risk_profile_form


urlpatterns = [
    path('', get_risk_profile, name='risk_profile'),
    path('risk-profile-form/', get_risk_profile, name='risk_profile_form'),
    path('risk-profile-form/submit/', submit_risk_profile_form, name='submit_risk_profile_form'),
    ]
