import json
import os

from data.distance import distance

def tradeoff_json(r, preference):
    problem_json = {"subject": "restaurant", "columns": [
        {
            "key": "rating",
            "type": "numeric",
            "goal": "max",
            "is_objective": False,
            "full_name": "Rating",
            "range": {
                "low": 4,
                "high": 5
            }
        },
        {
            "key": "distance_ray",
            "type": "numeric",
            "goal": "max",
            "is_objective": True,
            "full_name": "Distance_ray",
            "range": {
                "low": 0.500000,
                "high": 10.000000
            }
        },
        {
            "key": "geolocation",
            "type": "numeric",
            "goal": "min",
            "is_objective": True,
            "full_name": "Distance_ray",
            "range": {
                "low": 0.2,
                "high": 4.0
            }
        }
    ], "options": []}

    for i in range(0, len(r)):
        restaurant = {
            "key": str(r[i].id),
            "name": r[i].title,
            "values": {
                "rating": r[i].rating,
                "distance_ray": r[i].distance_ray,
                "geolocation": distance(float(r[i].latitude), float(r[i].longitude), 52.3416584, 4.888906)
            }
        }
        problem_json['options'].append(restaurant)

    #print(json.dumps(problem_json[0], indent=2, cls=DecimalEncoder))

    with open(os.path.join(os.path.dirname(__file__), '../resources/data.json'), 'w') as f:
        json.dump(problem_json, f, indent=2)

    return json.dumps(problem_json)