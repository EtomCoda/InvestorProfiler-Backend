from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from collections import defaultdict
from .models import FundCategory


# Create your views here.
@csrf_exempt
def get_fund_profile(request):
    if request.method == 'GET':
        # Prepare a dictionary to group categories by risk profile
        fund_data = defaultdict(list)

        # Prefetch related funds and risk profiles for efficiency
        categories = FundCategory.objects.prefetch_related('funds').select_related('risk_profile')

        for category in categories:
            profile_name = category.risk_profile.name
            fund_list = list(category.funds.values_list('name', 'score'))

            fund_data[profile_name].append({
                "category": category.name,
                "percent": category.percent,
                "funds": fund_list,

            })
        print('fund_data from funds VIEWS NOW', fund_data)
        return JsonResponse(dict(fund_data))