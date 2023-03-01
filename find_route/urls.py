from django.contrib import admin
from django.urls import path, include
from routes.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('find_routes/', find_routes, name='find_routes'),
    path('add_route/', add_route, name='add_route'),
    path('cities/', include(('cities.urls', 'cities'))),
    path('trains/', include(('trains.urls', 'trains'))),
]
