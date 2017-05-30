from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^get_idiom_of_the_day/(?P<curr_date>[\w\-]+)/$', views.get_idiom_of_the_day, name='get_idiom_of_the_day'),
]
