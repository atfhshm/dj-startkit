"""
This module contains shared model mixins for extending Django models with reusable functionality.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModelMixin(models.Model):
    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_("updated at"),
        auto_now=True,
    )

    class Meta:
        abstract = True


class DeletedModelMixin(models.Model):
    is_deleted = models.BooleanField(
        _("is deleted"),
        default=False,
        db_index=True,
    )
    deleted_at = models.DateTimeField(
        _("deleted at"),
        blank=True,
        null=True,
    )
    deleted_by = models.ForeignKey(
        "user.User",
        verbose_name=_("deleted by"),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="+",
    )

    class Meta:
        abstract = True
