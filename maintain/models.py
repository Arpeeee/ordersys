from django.db import models
from machine.models import Machine
from django.contrib.auth.models import User

class QualityTest(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, verbose_name='機器')
    name = models.CharField(max_length=100, verbose_name='品質測試名稱')
    description = models.TextField(null=True, blank=True, verbose_name='品質測試描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='建立者')
    file0 = models.FileField(null=True, blank=True, upload_to='quality_test/', verbose_name='品質測試檔案')
    # TODO 確認溫度
    temp1 = models.FloatField(null=True, blank=True, verbose_name='第一校正回溫')
    temp2 = models.FloatField(null=True, blank=True, verbose_name='第一校正轉黃溫度')
    temp3 = models.FloatField(null=True, blank=True, verbose_name='第一校正爆裂溫度')
    temp4 = models.FloatField(null=True, blank=True, verbose_name='校正後回溫')
    temp5 = models.FloatField(null=True, blank=True, verbose_name='校正後轉黃溫度')
    temp6 = models.FloatField(null=True, blank=True, verbose_name='校正後爆裂溫度')

    def show_date(self):
        return self.created_at.strftime('%Y-%m-%d')

    def __str__(self):
        return f"{self.machine} - {self.show_date()}"

    class Meta:
        verbose_name = '品質測試'
        verbose_name_plural = '品質測試'

class Mission(models.Model):
    name = models.CharField(max_length=255, verbose_name='維修/保養項目名稱')
    description = models.TextField(verbose_name='說明')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')

    def __str__(self):
        return f"{self.name} - {self.description}"

    class Meta:
        verbose_name = '維修/保養項目'
        verbose_name_plural = '維修/保養項目'
    
class MissionMaintain(models.Model):
    MISSION_STATUS_CHOICES = [
        (1, '未開始'),
        (2, '進行中'),
        (3, '已完成'),
    ]
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, verbose_name='維修/保養項目')
    maintain = models.ForeignKey('Maintain', on_delete=models.CASCADE, verbose_name='維護')
    description = models.TextField(verbose_name='維修/保養項目描述')
    status = models.IntegerField(choices=MISSION_STATUS_CHOICES, verbose_name='任務狀態')
    start_time = models.DateTimeField(null=True, blank=True, verbose_name='任務開始時間')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='任務結束時間')

    def __str__(self):
        return f"{self.maintain.machine.name} - {self.mission.name} - {self.status}"

    class Meta:
        verbose_name = '維修/保養任務'
        verbose_name_plural = '維修/保養任務'

class Maintain(models.Model):
    MAINTAIN_TYPE_CHOICES = [
        (1, '定期保養'),
        (2, '大保養'),
        (3, '小保養'),
    ]
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, verbose_name='機器')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='建立者')
    maintain_type = models.IntegerField(choices=MAINTAIN_TYPE_CHOICES, verbose_name='維護類型')
    missions = models.ManyToManyField(Mission, verbose_name='維修/保養項目', through='MissionMaintain')
    
    def __str__(self):
        return f"{self.machine.name} - {self.maintain_type}"

    class Meta:
        verbose_name = '維護紀錄'
        verbose_name_plural = '維護紀錄'
        unique_together = ('machine', 'created_at')
