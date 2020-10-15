from django.urls import path
from . import views

app_name = 'trip'

urlpatterns = [
    path('list', views.trip_list),
    path('chk/<str:name>', views.checkID),
    path('idealtag', views.idealtag),
    path('idealcategory', views.idealcategory),
    path('store_detail/<int:store_pk>', views.store_detail),
    path('today', views.trip_today),
    path('delete/<int:trip_pk>', views.delete_trip),
    path('date_chk', views.date_chk),
    path('delete/date_chk', views.delete_date_chk),
]