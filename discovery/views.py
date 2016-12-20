import decimal
import json
import datetime
import os
from math import radians, cos, sin, asin, sqrt

from django.http import HttpResponse
from django.http import HttpResponseServerError
from watson_developer_cloud.tradeoff_analytics_v1 import TradeoffAnalyticsV1
from watson_developer_cloud import PersonalityInsightsV3
from data.donwload_twitter_timeline import get_twitter_data

from discovery.models import Preferences
from discovery.models import Restaurants
from discovery_backend.settings.base import VCAP_SERVICES
from django_auth0.auth_backend import login_required

postgresql_credentials_env = VCAP_SERVICES['postgresql'][0]['credentials']

@login_required
def index(request):
    return HttpResponse(
        json.dumps({'response': "Hello, world. You're at the discovery index."})
    )

# /squares?category=
@login_required
def squares(request):
    # [52.371386, 4.896544] latitude, longitude random spot in the city center
    usr_id = (request.user['sub']).split('|')[1]

    # Get the category from the user
    category = str(request.GET['category'])
    latitude = float(request.GET['lat'])
    longitude = float(request.GET['lon'])

    # Select the restaurant based on the category selected
    rist = Restaurants.objects.filter(type=category)


    """
    # Get the tweets from the user
    #tweets = get_twitter_data(usr_id)
    tweets = get_twitter_data('74159038')

    personality_json = [{"contentItems": []}]
    for i in range(0, len(tweets[0])):
        data = {
            "content": tweets[0][i],
            "contenttype": "text/plain",
            "created": int(datetime.datetime.now().strftime("%s")) * 1000,
            "id": str(i),
            "language": "en"
        }
        personality_json[0]['contentItems'].append(data)

    with open(os.path.join(os.path.dirname(__file__), '../resources/personality.json'), 'w') as f:
        json.dump(personality_json[0], f, indent=2)

    personality_insights = PersonalityInsightsV3(
        username=VCAP_SERVICES['personality_insights'][0]['credentials']['username'],
        password=VCAP_SERVICES['personality_insights'][0]['credentials']['password']
    )

    # WATSON PERSONALITY INSIGHT
    with open(os.path.join(os.path.dirname(__file__), '../resources/personality.json')) as profile_json:
        profile = personality_insights.profile(
            profile_json.read(),
            content_type='application/json',
            raw_scores=True,
            consumption_preferences=True
        )
        #print(json.dumps(profile, indent=2))

    """

    problem_json = {
        "subject": "restaurant",
        "columns": [
            {
                "key": "rating",
                "type": "numeric",
                "goal": "max",
                "is_objective": True,
                "full_name": "Rating",
                "range": {
                    "low": 0,
                    "high": 5
                }
            },
            {
                "type": "numeric",
                "key": "distance_ray",
                "range": {
                    "low": 0.0,
                    "high": 40.0
                },
                "is_objective": True,
                "goal": "max",
                "full_name": "Distance_ray"
            },
            {
                "key": "geolocation",
                "type": "numeric",
                "goal": "min",
                "is_objective": True,
                "full_name": "Distance_ray",
                "range": {
                    "low": 0.0,
                    "high": 50.0
                }
            }
        ],
        "options": []
    }

    for i in range(0, len(rist)):
        restaurant = {
            "key": str(rist[i].id),
            "name": rist[i].title,
            "values": {
                "rating": rist[i].rating,
                "distance_ray": float(rist[i].distance_ray),
                "geolocation": distance(float(rist[i].latitude), float(rist[i].longitude), latitude, longitude)
            }
        }
        problem_json['options'].append(restaurant)

    # WATSON TRADEOFF ANALYTICS
    tradeoff_analytics = TradeoffAnalyticsV1(
        username = VCAP_SERVICES['tradeoff_analytics'][0]['credentials']['username'],
        password = VCAP_SERVICES['tradeoff_analytics'][0]['credentials']['password']
    )
    results = tradeoff_analytics.dilemmas(json.loads(json.dumps(problem_json)), generate_visualization=False)

    restaurants = []
    # Return results to the frontend

    for item in results['resolution']['solutions']:
        if item['status'] == "FRONT":
            idoneo = Restaurants.objects.get(id=int(item['solution_ref']))
            restaurants.append({
                "id": idoneo.id,
                "title": idoneo.title,
                "description": idoneo.description,
                "imgUrl": idoneo.imgUrl
            })
    print(json.dumps(restaurants, indent=2))

    return HttpResponse(
        json.dumps(restaurants, indent=2)
    )

# /details?id=54
@login_required
def details(request):
    restaurant_id = request.GET['id']
    r = Restaurants.objects.get(id=restaurant_id)
    return HttpResponse(json.dumps(r.as_dict()))

# /user_preferences
@login_required
def user_preferences(request):
    usr_id = (request.user['sub']).split('|')[1]

    # GET DATA
    if request.method == 'GET':
        preferences, created = Preferences.objects.get_or_create(userid=usr_id)
        return HttpResponse(json.dumps(preferences.as_dict()))

    # UPDATE DATA
    elif request.method == 'POST':
        json_data = json.loads(request.body.decode())  # request.raw_post_data w/ Django < 1.4

        try:
            restaurant, created = Preferences.objects.get_or_create(userid=usr_id)
            restaurant.italian = json_data['italian']
            #restaurant.mexican = json_data['mexican']
            restaurant.japanese = json_data['japanese']
            restaurant.greek = json_data['greek']
            restaurant.american = json_data['american']
            restaurant.indian = json_data['indian']
            restaurant.french = json_data['french']
            restaurant.chinese = json_data['chinese']
            restaurant.spanish = json_data['spanish']
            restaurant.indonesian = json_data['indonesian']
            restaurant.dutch = json_data['dutch']
            restaurant.argentinian = json_data['argentinian']
            restaurant.pakistanese = json_data['pakistanese']
            restaurant.african = json_data['african']
            restaurant.vietnamese = json_data['vietnamese']
            restaurant.pancakes = json_data['pancakes']
            restaurant.international = json_data['international']
            restaurant.save()

        except KeyError:
            return HttpResponseServerError(json.dumps({
                'error': 'malformed data'
            }))
        return HttpResponse({
            'result': 'preferences updated'
        })


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def distance(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km