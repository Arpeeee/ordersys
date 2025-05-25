from django.contrib.gis.db import models
from django.contrib.auth.models import User
# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name='聯絡人姓名')
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, verbose_name='客戶')
    email = models.EmailField(unique=True, verbose_name='聯絡人Email')
    email2 = models.EmailField(null=True, blank=True, verbose_name='聯絡人Email2')
    phone = models.CharField(max_length=10, verbose_name='聯絡人電話')
    phone2 = models.CharField(max_length=10, null=True, blank=True, verbose_name='聯絡人電話2')
    is_active = models.BooleanField(default=True, verbose_name='是否啟用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間')

    def __str__(self):
        return f"{self.customer.name} - {self.name} - {self.phone}"

    class Meta:
        ordering = ['name']
        verbose_name = '聯絡人資訊'
        verbose_name_plural = '聯絡人資訊'

class Customer(models.Model):
    name = models.CharField(max_length=100, verbose_name='公司名稱')
    address = models.TextField(verbose_name='公司地址')
    geo = models.PointField(null=True, blank=True, verbose_name='公司座標')
    address2 = models.TextField(null=True, blank=True, verbose_name='公司地址2')
    is_active = models.BooleanField(default=True, verbose_name='是否啟用')
    is_agent = models.BooleanField(default=False, verbose_name='是否代理商')
    tax_number = models.CharField(max_length=100, null=True, blank=True, verbose_name='統一編號')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間')

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = '客戶資訊'
        verbose_name_plural = '客戶資訊'

class Order(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, verbose_name='客戶')
    # TODO 確認一單會有幾個機器，是只有型號還是連機器序號也會有
    machine = models.ForeignKey('machine.Machine', on_delete=models.CASCADE, verbose_name='機器')
    order_number = models.CharField(max_length=100, verbose_name='訂單號碼')
    location = models.CharField(max_length=100, verbose_name='訂單地點')
    location_geo = models.PointField(null=True, blank=True, verbose_name='訂單地點座標')
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='訂單日期')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='建立者')

    def __str__(self):
        return f"{self.customer.name} - {self.order_number} - {self.order_date}"
    
    class Meta:
        verbose_name = '訂單紀錄'
        verbose_name_plural = '訂單紀錄'
