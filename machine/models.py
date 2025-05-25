from django.db import models
from django.contrib.auth.models import User
class Circuit(models.Model):
    COLOR_CHOICES = [
        (1, '紅'),
        (2, '綠'),
        (3, '藍'),
        (4, '黃'),
        (5, '紫'),
        ]
    number = models.CharField(max_length=100, verbose_name='電路版編號')
    description = models.TextField(verbose_name='電路描述')
    version = models.CharField(max_length=100, verbose_name='電路版版本')
    color = models.IntegerField(choices=COLOR_CHOICES, verbose_name='電路版顏色')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='建立者')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '電路板'
        verbose_name_plural = '電路板'

    def __str__(self):
        return f"{self.number} - {self.version} - {self.color}"

class CircuitUpgrade(models.Model):
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE, verbose_name='電路版')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='更新者')
    description = models.TextField(verbose_name='電路升級描述')
    file0 = models.FileField(upload_to='circuit_upgrade/', verbose_name='電路升級檔案')

    def __str__(self):
        return f"{self.circuit.name} - {self.updated_at}"

    class Meta:
        verbose_name = '電路板升級'
        verbose_name_plural = '電路板升級'

class Machine(models.Model):
    TYPEOF_CHOICES = [
        (1, '木頭'),
        (2, '鋼鐵'),
        (3, '鋁'),
        (4, '其他'),
    ]
    sn = models.CharField(max_length=100, unique=True, primary_key=True, verbose_name='機器序號')
    name = models.CharField(max_length=100, verbose_name='機器名稱')
    typeof = models.IntegerField(choices=TYPEOF_CHOICES, verbose_name='機器類型')
    generation = models.IntegerField(verbose_name='機器世代')
    number = models.IntegerField(blank=False, null=False, verbose_name='流水號')
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE, verbose_name='電路版')
    remote_id = models.CharField(max_length=100,blank=False, null=False, verbose_name='遠端機器序號')
    mac = models.CharField(max_length=100,blank=False, null=False,verbose_name='MAC')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='建立者')
    warranty_start_date = models.DateField(verbose_name='保固開始日期')
    warranty_end_date = models.DateField(verbose_name='保固結束日期')
    warranty_status = models.BooleanField(default=False, verbose_name='保固狀態')
    description = models.TextField(verbose_name='機器描述')


    class Meta:
        ordering = ['-created_at']
        verbose_name = '機器'
        verbose_name_plural = '機器'

    def __str__(self):
        return f"{self.sn} - {self.name} - {self.number} - {self.circuit}"

class TemperatureSensor(models.Model):
    TYPE_CHOICES = [
        (1, '第一象限'),
        (2, '風口'),
        (3, '第三象限'),
        (4, '第四象限'),
    ]
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, verbose_name='機器')
    name = models.CharField(max_length=100, verbose_name='溫度感測器名稱')
    parameter_file = models.FileField(upload_to='temperature_sensor/', verbose_name='溫度感測器參數檔案')
    description = models.TextField(verbose_name='溫度感測器描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    type = models.IntegerField(choices=TYPE_CHOICES, verbose_name='溫度感測器類型')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '溫度感測器'
        verbose_name_plural = '溫度感測器'

    def __str__(self):
        return f"{self.machine} - {self.name} - {self.type}"

class QualityTest(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, verbose_name='機器')
    name = models.CharField(max_length=100, verbose_name='品質測試名稱')
    description = models.TextField(verbose_name='品質測試描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='建立者')
    file0 = models.FileField(upload_to='quality_test/', verbose_name='品質測試檔案')
    # TODO 確認溫度
    temp1 = models.FloatField(verbose_name='第一溫度')

    def show_date(self):
        return self.created_at.strftime('%Y-%m-%d')

    def __str__(self):
        return f"{self.machine} - {self.show_date()}"

    class Meta:
        verbose_name = '品質測試'
        verbose_name_plural = '品質測試'