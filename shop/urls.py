from django.urls import path

from shop.views import *

app_name = 'shop'

urlpatterns = [

    path('buy_contract', buy_contract),
    path('deploy_contract', deploy_contract),
    path('make_wallet',make_wallet),
    path('<id>/update', product_update),
    path('write_sub', write_sub),
    path('write/', product_write),
    path('', product_in_category, name='product_all'),
    path('<slug:category_slug>/', product_in_category, name='product_in_category'),
    path('<int:id>/<product_slug>', product_detail, name='product_detail'),
]