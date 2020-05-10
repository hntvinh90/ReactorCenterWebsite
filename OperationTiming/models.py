from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from math import log
from datetime import datetime


USING_DATABASE = 'operation_timing'


# Create your models here.
class OperationTime(models.Model):
    date = models.DateField()
    from_time = models.TimeField()
    to_time = models.TimeField(blank=True)
    power = models.FloatField()

    # Cong suat record truoc
    from_power = models.FloatField(default=0)

    # Thoi gian de tinh chay (minutes)
    time_for_Mwd_up = models.FloatField(default=0)  # Thoi gian len cong suat
    time_for_Mwd_steady = models.FloatField(default=0)  # Thoi gian duy tri cong suat

    # Tinh chay
    MWd_up = models.FloatField(default=0)
    MWd_steady = models.FloatField(default=0)
    MWd_total = models.FloatField(default=0)

    # Thoi gian van hanh (minutes)
    operation_time_up = models.IntegerField(default=0)  # Thoi gian len cong suat
    operation_time_steady = models.IntegerField(default=0)  # Thoi gian duy tri cong suat


# Ngan chan cac ham su ly thuc thi khi database dang duoc truy cap
busy = False


# Xu ly truoc khi tao record moi
@receiver(pre_save, sender=OperationTime)
def pre_create_record(sender, instance, **kwargs):
    global busy

    if busy:
        return
    busy = True

    new_record = instance

    start_time = datetime.combine(new_record.date, new_record.from_time)
    stop_time = datetime.combine(new_record.date, new_record.to_time)

    # Load data of last record
    last_record = SaveData.get_last_record()

    # Neu last_record.power > 0 thi update cac gia tri steady
    if last_record and last_record.power:
        last_time = datetime.combine(last_record.date, last_record.to_time)

        # Thoi gian duy tri cong suat cua last record
        last_record.time_for_Mwd_steady = (start_time - last_time).total_seconds() / 60
        last_record.operation_time_steady = last_record.time_for_Mwd_steady

        # Tinh gia tri MWd_steady
        last_record.MWd_steady = last_record.time_for_Mwd_steady * last_record.power / 1440000

        # total MWd
        last_record.MWd_total += last_record.MWd_steady

        # save
        last_record.save()

    if new_record.power:
        t_up = (stop_time - start_time).total_seconds() / 60
        if last_record and last_record.power:
            if new_record.power == last_record.power:
                new_record.time_for_Mwd_up = t_up
            else:
                new_record.time_for_Mwd_up = t_up * log(2) / abs(log(
                    new_record.power / last_record.power
                )) / log(2) * abs(1 - last_record.power / new_record.power)

            # Neu last_record.power > 0 thi thoi gian t_up duoc tinh vao thoi gian van hanh
            new_record.operation_time_up = t_up
        else:
            new_record.time_for_Mwd_up = 1 / log(2)
        new_record.MWd_up = new_record.time_for_Mwd_up * new_record.power / 1440000

    new_record.MWd_total = new_record.MWd_up + last_record.MWd_total if last_record else 0

    if last_record:
        # set pk tiep theo la pk cua last record
        new_record.pk = last_record.pk + 1
        # from_power la cong suat cua last_record
        new_record.from_power = last_record.power
    else:
        # Neu la record dau tien
        new_record.pk = 1
        new_record.from_power = 0


# Xu ly sau khi tao record moi
@receiver(post_save, sender=OperationTime)
def save_record(sender, instance, **kwargs):
    new_record = instance

    # Luu lai record moi
    SaveData.save_last_record(new_record)

    global busy
    busy = False


# Xu ly sau khi xoa 1 record
@receiver(post_delete, sender=OperationTime)
def delete_record(sender, instance, using, **kwargs):
    global busy
    if busy:
        return
    busy = True

    # Xoa nhung record phia sau
    sender.objects.using(using).filter(pk__gt=instance.pk).delete()

    # Edit lai record con lai cuoi cung
    # Luu lai record do
    try:
        last_record = sender.objects.using(using).all().last()
        if last_record:
            last_record.time_for_Mwd_steady = 0
            last_record.MWd_total -= last_record.MWd_steady
            last_record.MWd_steady = 0
            last_record.operation_time_steady = 0
            last_record.save()

            # Save
            SaveData.save_last_record(last_record)
    except: pass

    busy = False


class SaveData(models.Model):
    """
    Luu lai gia tri cua record gan nhat
    """

    last_record = models.ForeignKey(OperationTime, on_delete=models.CASCADE)

    @staticmethod
    def get_last_record():
        global USING_DATABASE
        try:
            return SaveData.objects.using(USING_DATABASE).get(pk=1).last_record
        except: pass
        return None

    @staticmethod
    def save_last_record(last_record):
        global USING_DATABASE
        SaveData.objects.using(USING_DATABASE).update_or_create(
            pk=1,
            defaults={'last_record': last_record}
        )

    @staticmethod
    def get_first_date():
        global USING_DATABASE
        try:
            return OperationTime.objects.using(USING_DATABASE).get(pk=1).date
        except:
            pass
        return None

    @staticmethod
    def get_last_date():
        global USING_DATABASE
        try:
            return SaveData.objects.using(USING_DATABASE).get(pk=1).last_record.date
        except:
            pass
        return None
