"""PipAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from PIP01app import endpoints

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', endpoints.health_check),
    path('riders/', endpoints.riders),
    path('senders/', endpoints.senders),
    path('sessions/', endpoints.sessions),
    path('senders/<str:email>/', endpoints.sender_get),
    path('senders/<str:email>/sessions/', endpoints.sender_session_get),
    path('riders/<str:email>/', endpoints.rider_get),
    path('riders/<str:email>/sessions/', endpoints.rider_get_session),
    path('token_ph_patch/', endpoints.rider_token_ph_patch),
    path('orders/', endpoints.orders_p),
    path('delete_orders/<str:code_order>/', endpoints.delete_order),
    path('get_address/<str:code_address>/', endpoints.address_get),
    path('get_address_wol/',endpoints.address_get_wol),
    path('tupla/<str:code_order>/',endpoints.delete_tupla),
    path("pacth_tupla/<str:code_order>/", endpoints.patch_tupla),
    path('get_orders_all/<str:code_sender>/',endpoints.get_orders_last_12_biweeklys),
    path('get_orders_bw/<str:code_sender>/', endpoints.get_orders_bw),
    #path('get_orders_bw/<str:code_sender>/<str:start_date>/<str:end_date>/', endpoints.get_orders_bw)
    path('get_orders_by_day/<str:code_sender>/',endpoints.get_orders_by_day),
    path('gains_get/<str:code_rider>/', endpoints.gains_get),
    path('get_profit_all/<str:code_rider>/',endpoints.get_profit_last_12_biweeklys),
    path('get_profit_bw/<str:code_rider>/', endpoints.get_profit_bw),
    path('get_profit_by_day/<str:code_rider>/',endpoints.get_profit_by_day),
    path('connect_post/', endpoints.connect_post),
    path('connect_patch/',endpoints.connect_patch),
    path('connect_get/',endpoints.connect_get),
    path('send_patch_deliver_time/', endpoints.patch_deliver_time),
    path('send_patch_deliver_rider/<str:code_order>/', endpoints.patch_deliver_rider),
    path('remove_connect/', endpoints.remove_connect),
    path('weather_get/',endpoints.weather_get),
    path('weather_patch/',endpoints.weather_patch),
    path('wolift_get/<str:street>/<str:gate>/',endpoints.wolift_get),
    path('wolift_post',endpoints.wolift_post)
]
