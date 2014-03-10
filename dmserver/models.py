# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Categories(models.Model):
    cid = models.BigIntegerField(primary_key=True)
    is_parent = models.IntegerField()
    name = models.TextField()
    parent_cid = models.BigIntegerField()
    class Meta:
        db_table = 'categories'

class Images(models.Model):
    img_id = models.IntegerField(primary_key=True)
    img_id_in_visebuy = models.IntegerField()
    product_id = models.BigIntegerField()
    pic_url = models.CharField(max_length=255L)
    pic_path = models.CharField(max_length=255L)
    img_type = models.CharField(max_length=1L)
    pri_color_12 = models.IntegerField(null=True, blank=True)
    pri_color_12_value = models.FloatField(null=True, blank=True)
    sec_color_12 = models.IntegerField(null=True, blank=True)
    sec_color_12_value = models.FloatField(null=True, blank=True)
    pri_color_128 = models.IntegerField(null=True, blank=True)
    pri_color_128_value = models.FloatField(null=True, blank=True)
    sec_color_128 = models.IntegerField(null=True, blank=True)
    sec_color_128_value = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = 'images'

class Labelqueries(models.Model):
    labelquery_id = models.IntegerField(primary_key=True)
    img_id = models.IntegerField()
    cid = models.BigIntegerField()
    ids_all_in_c = models.TextField()
    ids_gw = models.TextField()
    ids_gc = models.TextField()
    ids_lw = models.TextField()
    ids_lc = models.TextField()
    ids = models.TextField()
    hit_gw = models.TextField()
    hit_gc = models.TextField()
    hit_lw = models.TextField()
    hit_lc = models.TextField()
    rank_gw = models.TextField()
    rank_gc = models.TextField()
    rank_lw = models.TextField()
    rank_lc = models.TextField()
    class Meta:
        db_table = 'labelqueries'

class Labels(models.Model):
    label_id = models.IntegerField(primary_key=True)
    labeluser_id = models.IntegerField()
    labelquery_id = models.IntegerField()
    page_id = models.IntegerField()
    imgids = models.TextField()
    labels = models.TextField()
    class Meta:
        db_table = 'labels'

class Labelusers(models.Model):
    labeluser_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=50L)
    password = models.CharField(max_length=50L)
    class Meta:
        db_table = 'labelusers'

class Products(models.Model):
    product_id = models.BigIntegerField(primary_key=True)
    cid = models.BigIntegerField()
    brand = models.CharField(max_length=20L)
    style = models.CharField(max_length=10L, blank=True)
    name = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField()
    product_url = models.CharField(max_length=255L)
    merchant = models.TextField()
    color = models.CharField(max_length=255L)
    recommendation = models.TextField()
    gender = models.CharField(max_length=3L)
    category = models.CharField(max_length=3L)
    class Meta:
        db_table = 'products'

class TmpImages(models.Model):
    img_id = models.IntegerField(primary_key=True)
    img_id_in_visebuy = models.IntegerField()
    product_id = models.BigIntegerField()
    pic_url = models.CharField(max_length=255L)
    pic_path = models.CharField(max_length=255L)
    img_type = models.CharField(max_length=1L)
    pri_color_12 = models.IntegerField(null=True, blank=True)
    pri_color_12_value = models.FloatField(null=True, blank=True)
    sec_color_12 = models.IntegerField(null=True, blank=True)
    sec_color_12_value = models.FloatField(null=True, blank=True)
    pri_color_128 = models.IntegerField(null=True, blank=True)
    pri_color_128_value = models.FloatField(null=True, blank=True)
    sec_color_128 = models.IntegerField(null=True, blank=True)
    sec_color_128_value = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = 'tmp_images'

