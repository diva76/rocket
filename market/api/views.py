# coding: utf8
from django.shortcuts import render
from json_response import JsonResponse
from api.models import *
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
