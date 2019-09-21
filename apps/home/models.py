# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    content_html = models.TextField(blank=True, null=True)
    add_time = models.DateTimeField(blank=True, null=True)
    platform = models.CharField(max_length=100, blank=True, null=True)
    platform_url = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
