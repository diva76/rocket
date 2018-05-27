# coding: utf8
from django.db import models
from pygments.lexers import get_all_lexers         # 一个实现代码高亮的模块 
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS]) # 得到所有编程语言的选项
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())     # 列出所有配色风格



#物品原始信息
class Product(models.Model):
    id = models.IntegerField(primary_key=True)    #条形码
    class_name = models.CharField(max_length=512) #物品分类
    unit = models.CharField(max_length=512) #商品单位
    extra = models.CharField(max_length=2048) #其他
    class Meta:
        db_table = 'product'

#商品
class Good(models.Model):
    id = models.AutoField(primary_key=True)
    item_code = models.CharField(max_length=512) #商品编号
    product_id = models.IntegerField(default=0)  #对应产品条码
    merchant_id = models.IntegerField(default=0) #商品对应商户
    store_id = models.IntegerField(default=0)    #商品对应门店
    status = models.IntegerField(default=0)      #商品状态，0-未上架；1-上架；2-下架；-2-删除
    class_name = models.CharField(max_length=512) #商品分类
    unit = models.CharField(max_length=512) #商品单位
    area = models.CharField(max_length=512) #产地
    shelf_day = models.DateTimeField() #有效期
    in_price = models.DecimalField(max_digits=19,decimal_places=2) #进价
    sale_price = models.DecimalField(max_digits=19,decimal_places=2) #销售价
    whole_sale_price = models.DecimalField(max_digits=19,decimal_places=2) #批发价
    vip_price = models.DecimalField(max_digits=19,decimal_places=2) #会员价
    remark = models.CharField(max_length=2048) #备注
    extra = models.CharField(max_length=2048) #其他
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'good'


#商户
class Merchant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=512)      #商户名称
    status = models.IntegerField(default=0)      #商户状态，0-待审核；1-有效；-1-审核拒绝；-2-删除
    shop_num = models.IntegerField(default=0)    #商户有多少家门店
    contact = models.CharField(max_length=512)   #商户联系人
    telephone = models.CharField(max_length=512) #商户联系电话
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'merchant'


#门店
class Store(models.Model):
    id = models.AutoField(primary_key=True)
    merchant_id = models.IntegerField(default=0) #门店对应商户id
    name = models.CharField(max_length=512)      #门店名称
    status = models.IntegerField(default=0)      #门店状态，0-待审核；1-有效；-1-审核拒绝；-2-删除
    location = models.CharField(max_length=2048) #门店地址
    latitude = models.DecimalField(max_digits=10,decimal_places=6,default=0)  #维度
    longitude = models.DecimalField(max_digits=10,decimal_places=6,default=0) #经度
    score = models.DecimalField(max_digits=2,decimal_places=1)      #评分
    icon = models.CharField(max_length=2048,default='')     #门店图片
    contact = models.CharField(max_length=512,default='')   #门店联系人
    telephone = models.CharField(max_length=512,default='')     #门店联系电话
    description = models.CharField(max_length=2048,default='')
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'store'

#顾客
class Custom(models.Model):
    id = models.AutoField(primary_key=True)
    custom_id = models.IntegerField(default=0)   #来自微信
    name = models.CharField(max_length=512)
    phone = models.CharField(max_length=512)
    wechat = models.CharField(max_length=512)
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'custom'
    

#优惠
class Benefit(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=512,default='')        #优惠券名称
    benefit_type = models.IntegerField(default=0) #优惠类型：1-商品直减；2-打折；3-满减
    type = models.IntegerField(default=0)         #优惠分类：1-商户优惠券（旗下所有门店通用）；2-门店优惠券
    value = models.CharField(max_length=512,default=0)	  #优惠值，benefit_type=1表示直减金额；benefit_type=2表示折扣数；benefit_type=3表示满减成都3/200
    related_id = models.IntegerField(default=0)   #相关id,type=1表示商户merchant_id;type=2表示store_id
    status = models.IntegerField(default=0)		  #优惠状态：0-无效；1-有效
    icon = models.CharField(max_length=512)      #优惠图片icon
    start_date = models.CharField(max_length=128,default='')			  #优惠开始时间
    end_date = models.CharField(max_length=128,default='')			  #优惠结束时间
    merchant_id = models.IntegerField(default=0)  #优惠对应商户id
    store_id = models.IntegerField(default=0)     #优惠对应门店id
    good_id = models.IntegerField(default=0)      #优惠对应商品id
    product_id = models.IntegerField(default=0)   #优惠对应物品id,如果type=1需要使用这个
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'benefit'


#交易明细表
class TradeInfo(models.Model):
    id = models.AutoField(primary_key=True)
    trade_id = models.IntegerField(default=0)    #交易号
    custom_id = models.IntegerField(default=0)    #顾客编号
    product_id = models.IntegerField(default=0)   #物品id
    good_id = models.IntegerField(default=0)      #商品id
    benefit_id = models.IntegerField(default=0)      #优惠id
    store_id = models.IntegerField(default=0)      #门店id
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'trade_info'

 
#订单与交易对应表  
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    custom_id = models.IntegerField(default=0)    #顾客编号
    trade_no = models.CharField(max_length=512)   #流水号
    trade_id = models.IntegerField(default=0)     #交易号
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'order'

#流水表
class PayDetail(models.Model):
    id = models.AutoField(primary_key=True)
    trade_no = models.CharField(max_length=512)   #流水号
    store_id = models.IntegerField(default=0)     #商铺
    way = models.IntegerField(default=0)          #支付方式：1-微信；2-支付宝。。。
    pay_time = models.DateTimeField(auto_now_add=True)  #支付时剑
    trade_status = models.IntegerField(default=0) #交易状态：？？
    fee = models.DecimalField(max_digits=19,decimal_places=2)  #支付金额
    refund_status = models.IntegerField(default=0) #退款状态
    extra = models.CharField(max_length=2048) #其他
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'pay_detail'


#用户预约优惠
class CustomBenifit(models.Model):
    id = models.AutoField(primary_key=True)
    custom_id = models.IntegerField(default=0)    #顾客编号
    good_id = models.IntegerField(default=0)      #商品编号
    product_id = models.IntegerField(default=0)   #物品编号
    benefit_id = models.IntegerField(default=0)   #优惠编号
    status = models.IntegerField(default=0)       #状态
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'custom_benefit'

