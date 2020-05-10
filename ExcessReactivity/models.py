from django.db import models

# Create your models here.
USING_DATABASE = 'excess_reactivity'


# Tat ca cac nam trong database
class ER_Years(models.Model):
    year = models.CharField(max_length=4)

    def __str__(self):
        return self.year


# Do phan ung du tru
class ExcessReactivity(models.Model):
    year = models.ForeignKey(ER_Years, models.CASCADE)
    date = models.CharField(max_length=32)

    # Vi tri cac thanh dieu khien va do phan ung du tru luc chua nap mau voi cs 0.5%
    power05_without_target_4SR = models.CharField(max_length=32, blank=True, verbose_name='Vị trí 4SR')
    power05_without_target_AR = models.CharField(max_length=32, blank=True, verbose_name='Vị trí AR')
    power05_without_target_ER = models.CharField(max_length=32, blank=True, verbose_name='Độ phản ứng dự trữ')

    # Vi tri cac thanh dieu khien va do phan ung du tru khi da nap mau voi cs 0.5%
    power05_4SR = models.CharField(max_length=32, blank=True, verbose_name='Vị trí 4SR')
    power05_AR = models.CharField(max_length=32, blank=True, verbose_name='Vị trí AR')
    power05_ER = models.CharField(max_length=32, blank=True, verbose_name='Độ phản ứng dự trữ')

    # Vi tri cac thanh dieu khien va do phan ung du tru dau dot voi cs 100%
    power100_start_4SR = models.CharField(max_length=32, blank=True, verbose_name='Vị trí 4SR')
    power100_start_AR = models.CharField(max_length=32, blank=True, verbose_name='Vị trí AR')
    power100_start_ER = models.CharField(max_length=32, blank=True, verbose_name='Độ phản ứng dự trữ')

    # Vi tri cac thanh dieu khien va do phan ung du tru cuoi dot voi cs 100%
    power100_end_4SR = models.CharField(max_length=32, blank=True, verbose_name='Vị trí 4SR')
    power100_end_AR = models.CharField(max_length=32, blank=True, verbose_name='Vị trí AR')
    power100_end_ER = models.CharField(max_length=32, blank=True, verbose_name='Độ phản ứng dự trữ')

    def __str__(self):
        return '%s - %s' % (self.year, self.date)
