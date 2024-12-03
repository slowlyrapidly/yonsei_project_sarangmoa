from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.timezone import now


# Create your models here.

def time_now():
    return timezone.now()

class Bible(models.Model):
    book_name=models.CharField(max_length=20)
    book_no=models.IntegerField(blank=True,null=True)

class User(models.Model):
    uid=models.AutoField(blank=False,null=False,primary_key=True)
    id=models.CharField(null=False,blank=False,max_length=20)
    pw=models.CharField(null=False,blank=False,max_length=20)
    name=models.CharField(null=False,blank=False,max_length=20)
    birth=models.IntegerField(blank=False,null=False)
    gender=models.CharField(null=False,blank=False,max_length=1,choices=[('M','남성'),('F','여성')])
    address=models.CharField(null=False,blank=False,max_length=20)
    mileage=models.IntegerField(null=False,blank=False,default=0)
    voluntary_point=models.IntegerField(null=False,blank=False,default=0)
    authorization = models.IntegerField(null=False,blank=False,default=0)
    cert_reg_img=models.ImageField(upload_to='cert_reg/',null=True)

    @property
    def is_authenticated(self):
        return True

class Product(models.Model):
    pid=models.AutoField(blank=False,null=False,primary_key=True)
    category=models.IntegerField(blank=False,null=False)
    p_name=models.CharField(null=False,blank=False,max_length=50)
    p_image=models.ImageField(upload_to='product_images/')
    cost=models.IntegerField(null=False,blank=False)
    description=models.CharField(null=False,blank=False,max_length=1000)
    status=models.IntegerField(null=False,blank=False, default=0)



class Uploaded_product(models.Model):
    uid=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    pid=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    created_date=models.DateField(null=False,blank=False,default=now)
    updated_date=models.DateField(null=False,blank=False,default=now)

class Buy_list(models.Model):
    seller_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='seller')
    buyer_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='buyer')
    pid = models.ForeignKey(Uploaded_product, on_delete=models.SET_NULL, null=True)  # Uploaded_product 참조
    buy_date = models.DateField(default=now)
    pay_method = models.IntegerField(default=0)


class Notice(models.Model):
    id=models.IntegerField(blank=False,null=False,primary_key=True)
    title=models.CharField(blank=False,null=False,max_length=30)
    content=models.CharField(blank=False,null=False,max_length=2000)
    count=models.IntegerField(blank=False,null=False,default=0)


class Event(models.Model):
    id=models.IntegerField(blank=False,null=False,primary_key=True)
    title=models.CharField(blank=False,null=False,max_length=30)
    content=models.CharField(blank=False,null=False,max_length=2000)
    event_image=models.ImageField(upload_to='event_images/',null=True)
    count=models.IntegerField(blank=False,null=False,default=0)
    mileage_price=models.IntegerField(blank=False,null=False,default=0)

class Event_User_List(models.Model):
    id=models.IntegerField(blank=False,null=False,primary_key=True)
    uid=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    event_id=models.ForeignKey(Event,on_delete=models.SET_NULL,null=True)


class GoodExamples(models.Model):
    id=models.IntegerField(blank=False,null=False,primary_key=True)
    event_image=models.ImageField(upload_to='good_example_images/',null=True)
    title = models.CharField(blank=False, null=False, max_length=30)
    content = models.CharField(blank=False, null=False, max_length=2000)
