from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^squares/$', views.squares, name='squares'),
    url(r'^details/$', views.details, name='details'),
    url(r'^user_preferences/$', views.user_preferences, name='user_preferences')
]
