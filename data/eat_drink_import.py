import csv
from discovery.models import Restaurants

r = csv.reader(open('resources/local_restaurants.csv'), delimiter=',')
for line in r:
    if line[0] == "id":
        continue
    print("{}: {}".format(line[0], line[1]))
    Restaurants.objects.create(title=line[1],
                               type=line[2],
                               description=line[3],
                               opening_hours=line[4],
                               city=line[5],
                               address=line[6],
                               zip_code=line[7],
                               min_price=line[8],
                               max_price=line[9],
                               latitude=line[10],
                               longitude=line[11],
                               rating=line[12],
                               url=line[13],
                               imgUrl=line[14],
                               distance_ray=line[15])
