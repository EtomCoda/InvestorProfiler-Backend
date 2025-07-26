from django.shortcuts import render
        # """
        # This Django view function receives a POST request with option IDs, calculates a risk profile based
        # on the provided IDs, and returns the profile's name and description in a JSON response.
        
        # :param request: The `request` parameter in the `get_risk_profile` function represents an HTTP
        # request that is sent to the server. It contains information about the request made by the client,
        # such as the request method (GET, POST, etc.), headers, body, and other metadata. In this context,
        # :return: The `get_risk_profile` view function returns a JSON response containing the risk profile
        # name and description based on the option IDs provided in the POST request data. If a matching
        # profile is found, it returns a JSON response with the profile name and description. If no matching
        # profile is found, it returns a JSON response with an error message indicating that no matching
        # profile was found. If there is a ValueError
        # """

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import calculate_risk_profile
from .utils import ShortTimeHorizonError

@csrf_exempt
def get_risk_profile(request):
    return render(request,'../templates/risk_form.html')

# this request sends the option ids to the server, which are then used to calculate the risk profile. The server processes the request and returns a JSON response containing the risk profile name and description.
@csrf_exempt
def submit_risk_profile_form(request):
    if request.method == 'POST':
        print('this is the req at views',request.POST)
        data = json.loads(request.body)

        print(data)
        selected = request.POST.getlist("q5")  # returns a list of strings: ['17', '18', '20']
        print(selected)
        option_ids = data.get('option_ids', [])
        
        #retrieves the list of option IDs from the request body.
        # This list represents the options selected by the user in response to the set of questions.

        try:
            profile = calculate_risk_profile(option_ids)
            if profile:
                print('PROFILE',profile)
                return JsonResponse({'profile': profile.name, 'description': profile.description})
            
            else:
                return JsonResponse({'error': 'No matching profile found'}, status=404)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except ShortTimeHorizonError as e:
            return JsonResponse({"error": str(e)}, status=400)
 

    return render(request, '../templates/fund_categories.html') 
