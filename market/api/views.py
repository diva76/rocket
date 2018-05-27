# coding: utf8
from django.shortcuts import render
from json_response import JsonResponse
from api.models import *
import json
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
#获取附近商店
@json_response
def shops_nearby(request):
    if request.method == 'GET':
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
    else:
        return {
            'status':403,
            'message':'fail',
            'data':"only support GET method"
        }

#获取选择门店列表
@json_response
def shops_all(request):
    if request.method == 'GET':
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
    else:
        return {
            'status':403,
            'message':'fail',
            'data':"only support GET method"
        }

#获取优惠券列表
@json_response
def shops_redeem_list(request):
    if request.method == 'GET':
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
    else:
        return {
            'status':403,
            'message':'fail',
            'data':"only support GET method"
        }

#领取优惠券
@json_response
def redeem_obtain(request):
    if request.method == 'POST':
        rsp = {
            'status': 200,
            'message': 'success',
            'data':""
        }
        redeem_id = int(request.POST.get('redeem_id', 0))   #优惠券id
        custom_id = int(request.POST.get('custom_id', 0))   #用户id

        c = CustomBenifit(custom_id=custom_id, benefit_id=redeem_id)
        c.save()
        return rsp
    else:
        return {
            'status':403,
            'message':'fail',
            'data':"only support post method"
        }

#扫码
# !!!!!!!预约礼包
@json_response
def scan_report (request):
    if request.method == 'POST':
        rsp = {
            'status': 200,
            'message': 'success',
            'data':{
                'product_info':{},
                'redeem_list':[]
            }
        }
        result  = request.POST.get('result', '')   #扫码的内容
        custom_id = request.POST.get('charSet', 0)   #扫码字符集
        store_id = request.POST.get('store_id', 0)   #商店id

        q = Good.objects.filter(product_id=result, store_id=store_id).query
        print q
        g = Good.objects.filter(product_id=result, store_id=store_id).first()
        if g is None:
            rsp['status'] = 404
            rsp['message'] = 'fail'
            return rsp
        rsp['data']['product_info'] = {
            'id': g.id,
            'name':g.name,
            'price': g.sale_price,
            'image': g.icon,
            'description': g.description
        }
        #获取商品本店的优惠
        today = datetime.now().strftime("%Y-%m-%d")
        today_date = "'{day}'".format(day=today)
        q=Benefit.objects.filter(store_id=store_id).filter(good_id=g.id).filter(status=1).filter(end_date__gte=today_date).query
        print q
        benefits = Benefit.objects.filter(store_id=store_id).filter(good_id=g.id).filter(status=1).filter(end_date__gte=today_date)
        for v in benefits:
            can_use = True
            if v.start_date > today_date:
                can_use = False
            rsp['data']['redeem_list'].append({
                'id': v.id,
                'name':v.name,
                'type':v.type,
                'benefit_type':v.benefit_type,
                'icon':v.icon,
                'product_id':v.product_id,
                'can_use': can_use,
                'redeem_number': v.value
            })
        return rsp
    else:
        return {
            'status':403,
            'message':'fail',
            'data':"only support post method"
        }

#结账
@json_response
def order_new (request):
    if request.method == 'POST':
        rsp = {
            'status': 200,
            'message': 'success',
            'data':{}
        }
        products = request.POST.get('product_list')
        custom_id = request.POST.get('custom_id')
        store_id = request.POST.get('store_id')
        product_list = json.loads(products)
        print product_list

        all_fee = 0.0
        fee = 0.0
        benefit_value = 0.0
        count=0
        today_date = datetime.now().strftime("%Y-%m-%d")
        for v in product_list:
            #q = Good.objects.filter(item_code=v['product_id']).filter(store_id=store_id).query
            #print q
            good = Good.objects.filter(item_code=v['product_id']).filter(store_id=store_id).first()
            if good is None:
                rsp['status']=404
                rsp['message'] ='fail'
                rsp['data'] = "商品{product_id}未录入".format(product_id=v['product_id'])
                return rsp
            good_id = good.id
            count+=int(v['count'])
            fee += float(good.sale_price)*v['count']
            all_fee += float(good.sale_price)*v['count']
            #获取用户领取的券
            c = CustomBenifit.objects.filter(custom_id=custom_id).filter(good_id=good_id)
            for v in c:
                good_id = v.good_id
                benefit_id = v.benefit_id
                b = Benefit.objects.filter(id=benefit_id).filter(status=1).filter(start_date__lte=today_date).filter(end_date__gte=today_date)
                if b is not None:
                    for v in b:
                        if v.benefit_type == 1: #直减优惠
                            benefit_value += float(v.value)
                            fee = fee - float(v.value)
                        elif v.benefit_type == 2:
                            benefit_value += float(good.sale_price) * (1-float(v.value))
                            fee = fee - float(good.sale_price) * (1-float(v.value))

            #通过fee调起支付获取交易order
            #记录订单记录
             #t = TradeInfo(custom_id=custom_id,)
            #流水
            p = PayDetail(trade_no='',store_id=store_id,way=1,trade_status=1,fee=fee)
            p.save()
            o = Order(custom_id=custom_id,trade_no='',count=count,paid_price=fee,total_price=all_fee,redeem_price=benefit_value,store_id=store_id)
            o.save()

            rsp['data'] = {
                'order_id':'',
                'pay_price': fee,
                'total_price':all_fee,
                'redeem_price': benefit_value 
            }
            return rsp
    else:
         return {
            'status':403,
            'message':'fail',
            'data':"only support post method"
        }

#我得订单列表
@json_response
def my_order(request):
    if request.method == 'GET':
        rsp = {
            'status': 200,
            'message': 'success',
            'data':{
                'order_list':[],
                'pagination':{}
            }
        }
        hasNext = True
        custom_id = int(request.GET.get('custom_id',0))
        page_size = int(request.GET.get('page_size',2)) #每页数量
        current = int(request.GET.get('current', 1))    #当前页数
        q = Order.objects.filter(custom_id=custom_id)[(current-1)*page_size: current*page_size].query
        print q
        result = Order.objects.filter(custom_id=custom_id)[(current-1)*page_size: current*page_size]
        if result is None:
            rsp['pagination'] = {
                'has_next': hasNext,
                'current': current,
                'page_size': page_size,
            }
            return rsp
        print result
        if len(result) < page_size+1:
            haseNext = False
        for i in range(0, len(result)):
            print result[i]
            rsp['data']['order_list'].append({
                'id':result[i].id,
                'name': result[i].store_id,
                'count': result[i].count,
                'paid_price': result[i].paid_price, 
                'total_price': result[i].total_price, 
                'redeem_price': result[i].redeem_price
            })
        rsp['data']['pagination'] = {
            'has_next': hasNext,
            'current': current,
            'page_size': page_size,
        }
        return rsp
    else:
        return {
            'status':403,
            'message':'fail',
            'data':"only support GET method"
        }

#订单详情
@json_response
def my_order(request):
    if request.method == 'GET':
        rsp = {
            'status': 200,
            'message': 'success',
            'data':{
                'product_list':[],
                'price':{}
            }
        }
        custom_id = int(request.GET.get('custom_id',0))
        order_id = int(request.GET.get('order_id',0)) #每页数量
        t = TradeInfo.objects.filter(trade_id=order_id).filter(custom_id=custom_id)
        if t is None:
            rsp['status']=404
            return rsp
        for v in t:
            rsp['data']['product_list'].append({
                'name':v.product_id,
                'image':'',
                'price':v.price,
                'count':v.count
            })
        o = Order.objects.filter(custom_id=custom_id).filter(trade_id=trade_id).first()
        if o is not None:
            rsp['data']['price'] = {
                'total_price': o.total_price,
                'paid_price': o.paid_price,
                'redeem_price': o.redeem_price,
                'store':o.store_id
            }
        return rsp
    else:
        return {
            'status':403,
            'message':'fail',
            'data':"only support GET method"
        }



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
