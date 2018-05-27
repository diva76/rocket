# coding: utf8
from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'shops/nearby$', views.shops_nearby),
    url(r'shops/all$', views.shops_all),
    url(r'redeem/list$', views.shops_redeem_list),
    url(r'redeem/obtain$', views.redeem_obtain),
    url(r'scan/report$', views.scan_report),
    url(r'order/new$', views.order_new),
    url(r'order/my$', views.my_order),
    url(r'order/detail$', views.order_detail),  
    url(r'^(?P<pk>[0-9]+)/$', views.json_view),
]
