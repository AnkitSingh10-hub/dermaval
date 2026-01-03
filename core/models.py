# from django.db import models
from django.contrib.gis.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from core.managers import *

# Create your models here.

class District(models.Model):
    gid = models.IntegerField(primary_key=True)
    geom = models.MultiPolygonField(blank=True, null=True)
    dcode = models.IntegerField(blank=True, null=True)
    scode = models.IntegerField(blank=True, null=True)
    sdd = models.FloatField(blank=True, null=True)
    length = models.FloatField(blank=True, null=True)
    area = models.FloatField(blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = "district"

    def __str__(self) -> str:
        return self.name


class Municipality(models.Model):
    geom = models.MultiPolygonField(blank=True, null=True)
    dcode = models.IntegerField(blank=True, null=True)
    district = models.CharField(max_length=254, blank=True, null=True)
    gapa_napa = models.CharField(max_length=254, blank=True, null=True)
    type_gn = models.CharField(max_length=254, blank=True, null=True)
    province = models.CharField(max_length=254, blank=True, null=True)
    nepali = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        db_table = "municipality"

    def __str__(self) -> str:
        return self.gapa_napa


class Province(models.Model):
    id = models.IntegerField(primary_key=True)
    geom = models.MultiPolygonField(blank=True, null=True)
    scode = models.IntegerField(blank=True, null=True)
    length = models.FloatField(blank=True, null=True)
    area = models.FloatField(blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = "province"

    def __str__(self) -> str:
        return self.name



class TimeStampedModel(models.Model):
    """
    Abstract model for adding timestamps.
    """

    date_created = models.DateTimeField(
        _("created date"), auto_now_add=True, null=True, blank=True
    )
    date_modified = models.DateTimeField(
        _("modified date"), auto_now=True, null=True, blank=True
    )

    class Meta:
        abstract = True

class SoftDeleteModal(models.Model):
    """
    Abstract model to handle soft deletion of data.
    """
    is_deleted = models.BooleanField(_("is deleted"), default=False)
    deleted_date = models.DateTimeField(_("deleted date"), null=True, blank=True)

    objects = SoftDeleteManager()

    class Meta:
        abstract = True

    def soft_delete(self, *args, **kwargs):
        """
        Soft delete the model instance.
        """
        if not self.is_deleted:
            self.is_deleted =True
            self.deleted_date = timezone.now()
            return super().save(*args, **kwargs)
        
    def restore(self, *args, **kwargs):
        """
        Restore(Undelete) only soft deleted instance.
        """
        if self.is_deleted:
            self.is_deleted = False
            self.deleted_date= None
            return super().save(*args, **kwargs)
        
     