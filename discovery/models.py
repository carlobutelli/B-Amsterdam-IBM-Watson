from __future__ import unicode_literals
import logging
from django.db import models

logger = logging.getLogger(__name__)


class Square:
    def __init__(self, square_id):
        self.id = square_id
        self.title = "ID: {}".format(self.id)
        self.subtitle = "This is square #{}".format(self.id)
        self.img_url = "//ckinknoazoro.files.wordpress.com/2011/06/random.jpg"

    def to_map(self):
        return {
            "id": self.id,
            "title": self.title,
            "subtitle": self.subtitle,
            "imgUrl": self.img_url
        }


class Restaurants(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(null=True, max_length=150)
    type = models.CharField(null=True, max_length=50)
    description = models.CharField(null=True, max_length=1000, db_column='short_description')
    opening_hours = models.CharField(null=True, max_length=250)
    city = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=100, null=True)
    zip_code = models.CharField(max_length=8, null=True)
    min_price = models.IntegerField()
    max_price = models.IntegerField()
    latitude = models.CharField(max_length=15, null=True)
    longitude = models.CharField(max_length=15, null=True)
    distance_ray = models.CharField(max_length=20, null=True)
    rating = models.IntegerField(null=False)
    url = models.CharField(null=True, max_length=500)
    imgUrl = models.CharField(null=True, max_length=200, db_column='imgurl')

    def __str__(self):
        return self.title

    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "type": self.type,
            "description": self.description,
            "opening_hours": self.opening_hours,
            "city": self.city,
            "address": self.address,
            "zip_code": self.zip_code,
            "min_price": self.min_price,
            "max_price": self.max_price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "distance_ray": self.distance_ray,
            "rating": self.rating,
            "url": self.url,
            "imgUrl": self.imgUrl
        }

    class Meta:
        db_table = 'restaurants'


class Preferences(models.Model):
    userid = models.BigIntegerField(primary_key=True)
    italian = models.BooleanField(default=False)
    mexican = models.BooleanField(default=False)
    japanese = models.BooleanField(default=False)
    greek = models.BooleanField(default=False)
    american = models.BooleanField(default=False)
    indian = models.BooleanField(default=False)
    french = models.BooleanField(default=False)
    chinese = models.BooleanField(default=False)
    spanish = models.BooleanField(default=False)
    indonesian = models.BooleanField(default=False)
    dutch = models.BooleanField(default=False)
    argentinian = models.BooleanField(default=False)
    pakistanese = models.BooleanField(default=False)
    african = models.BooleanField(default=False)
    vietnamese = models.BooleanField(default=False)
    pancakes = models.BooleanField(default=False)
    international = models.BooleanField(default=False)

    def as_dict(self):
        return {
            "userid": self.userid,
            "italian": self.italian,
            "mexican": self.mexican,
            "japanese": self.japanese,
            "greek": self.greek,
            "american": self.american,
            "indian":self.indian,
            "french": self.french,
            "chinese": self.chinese,
            "spanish": self.spanish,
            "indonesian": self.indonesian,
            "dutch": self.dutch,
            "argentinian": self.argentinian,
            "pakistanese": self.pakistanese,
            "african": self.african,
            "vietnamese": self.vietnamese,
            "pancakes": self.pancakes,
            "international": self.international
        }


    class Meta:
        db_table = 'preferences'