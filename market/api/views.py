# coding: utf8
from django.shortcuts import render
from json_response import JsonResponse
from api.models import *
import random
from datetime import datetime
# Create your views here.
from json_response import json_response, jsonp_response, auto_response
'''
def json_view(request):


    objs = Merchant.objects.all()

    return JsonResponse({
        'status': 200,
        'message': u'成功',
        'data': {
            'data1': 'xxx',
            'data2': 'ooo',
            'objs': [obj.data for obj in objs]
        }
    })
'''
@json_response
def shops_nearby(request):
    rsp = {
        'status': 200,
        'message': 'success',
        'data':{
            'shop_list':[],
            'pagination':{}
        }
    }
    hasNext = True
    latitude = float(request.GET.get('latitude', 0))   #维度
    longitude = float(request.GET.get('longitude', 0)) #经度
    page_size = int(request.GET.get('page_size',2)) #每页数量
    current = int(request.GET.get('current', 1))    #当前页数

    q = Store.objects.all()[(current-1)*page_size: current*page_size].query
    print q
    result = Store.objects.all()[(current-1)*page_size: current*page_size]
    if len(result) == 0:
        rsp['pagination'] = {
            'has_next': hasNext,
            'current': current,
            'page_size': page_size,
        }
        return rsp
    if len(result) < page_size+1:
        haseNext = False
    for i in range(0, len(result)):
        v = "{x}".format(x=int(random.random()*1000))
        distance = "{distance}m".format(distance=v)
        store_id = result[i].id
        count = Benefit.objects.filter(store_id=store_id).filter(status=1).count()
        rsp['data']['shop_list'].append({
            'name': result[i].name,
            'distance': distance,
            'score': 5,
            'description': result[i].description,
            'redeem_count':count,
        })
    rsp['pagination'] = {
        'has_next': hasNext,
        'current': current,
        'page_size': page_size,
    }
    return rsp

@json_response
def shops_all(request):
    rsp = {
        'status': 200,
        'message': 'success',
        'data':{
            'nearby_shop_list':[],
            'history_shop_list':[],
            'all_shop_list':[]
        }
    }
    latitude = float(request.GET.get('latitude', 0))   #维度
    longitude = float(request.GET.get('longitude', 0)) #经度

    q = Store.objects.all().query
    print q
    result = Store.objects.all()
    if len(result) == 0:
        return rsp
    for i in range(0, len(result)):
        v = "{x}".format(x=int(random.random()*1000))
        distance = "{distance}m".format(distance=v)
        store_id = result[i].id
        count = Benefit.objects.filter(store_id=store_id).filter(status=1).count()
        shop_info = {
            'name': result[i].name,
            'distance': distance,
            'score': 5,
            'description': result[i].description,
            'redeem_count':count,
        }
        rsp['data']['nearby_shop_list'].append(shop_info)
        rsp['data']['history_shop_list'].append(shop_info)
        rsp['data']['all_shop_list'].append(shop_info)
    return rsp

@json_response
def shops_redeem_list(request):
    rsp = {
        'status': 200,
        'message': 'success',
        'data':{
            'redeem_list':[],
            'pagination':{}
        }
    }
    hasNext = True
    latitude = float(request.GET.get('latitude', 0))   #维度
    longitude = float(request.GET.get('longitude', 0)) #经度
    shop_id = int(request.GET.get('shop_id', 0))
    status = int(request.GET.get('status', 0))
    page_size = int(request.GET.get('page_size', 2))
    current = int(request.GET.get('current', 1))

    today_date = datetime.now().strftime("%Y-%m-%d")
    today_date = "'{day}'".format(day=today_date)
    q = Benefit.objects.filter(store_id=shop_id).filter(status=1).filter(start_date__lte=today_date).filter(end_date__gte=today_date)[(current-1)*page_size: current*page_size].query
    print q
    print '==='
    result = Benefit.objects.filter(store_id=shop_id)#.filter(status=1).filter(start_date__lte=today_date).filter(end_date__gte=today_date)#[(current-1)*page_size: current*page_size]
    print '!!!!!'
    print result
    if len(result) == 0 or shop_id==0:
        rsp['pagination'] = {
            'has_next': hasNext,
            'current': current,
            'page_size': page_size,
        }
        return rsp
    if len(result) < page_size+1:
        haseNext = False
    for i in range(0, len(result)):
        good_price = 0
        good = Good.objects.filter(id=result[i].good_id)
        if len(good) > 0:
            good_price = good[0].sale_price
        #good_price = good.sale_price
        if result[i].benefit_type ==2:
            unit = "zhe"
        else:
            unit="yuan"
        if result[i].type == 1:
            m = Merchant.objects.filter(id=result[i].merchant_id)
            shop = m[0].name
        else:
            s = Store.objects.filter(id=result[i].store_id)
            shop = s[0].name
        rsp['data']['redeem_list'].append({
            'name': result[i].name,
            'type': result[i].benefit_type, #1-商品直减；2-打折；3-满减
            'price':good_price,
            'redeem_number': result[i].value,
            'redeem_unit':unit,
            'redeem_shop': shop,
            'left_redeem_coutn': int(random.random()*100),
            #'end_date': result[i].end_date,
        })
    rsp['pagination'] = {
        'has_next': hasNext,
        'current': current,
        'page_size': page_size,
    }
    print rsp
    return rsp

@json_response
def json_view(request):
    page_num=request.GET.get('page')
    content=request.GET.get('content')
    objs = Merchant.objects.all()

    return {
        'status': 200,
        'message': u'成功',
        'data': {
            'data1': 'xxx',
            'data2': 'ooo',
            'objs': [obj.data for obj in objs]
        }
    }
