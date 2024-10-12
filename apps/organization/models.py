import secrets
from uuid import uuid4

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from apps.user.models import User
from core.models import TimeStampedModelMixin


class Organization(TimeStampedModelMixin):
    class OrganizationStatus(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        SUSPENDED = "SUSPENDED", "Suspended"

    name = models.CharField(
        _("name"),
        max_length=64,
        db_index=True,
    )
    slug = models.SlugField(
        _("slug"),
        max_length=84,
        unique=True,
        db_index=True,
        editable=False,
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("owner"),
        related_name="owned_organizations",
    )
    avatar = models.ImageField(
        verbose_name=_("avatar"),
        upload_to="organization/",
    )
    status = models.CharField(
        _("status"),
        choices=OrganizationStatus.choices,
        default=OrganizationStatus.ACTIVE,
        db_index=True,
    )
    country = CountryField(
        verbose_name=_("country"),
        db_index=True,
    )

    class Meta:
        db_table = "organizations"
        verbose_name = _("organization")
        verbose_name_plural = _("organizations")
        ordering = ("-id",)

    def __str__(self) -> str:
        return f"{self.slug!s}"

    def save(self, *args, **kwargs):
        # FIXME: Not the cleanest implementation (refactor later)
        if not self.pk:
            slug = slugify(
                self.name,
                allow_unicode=True,
            )
            org = Organization.objects.filter(slug=slug).first()
            if org:
                self.slug = slugify(
                    self.name + " " + secrets.token_hex(2),
                    allow_unicode=True,
                )
            else:
                self.slug = slug

        org = Organization.objects.filter(pk=self.pk).first()
        if (org) and (org.name != self.name):
            self.slug = slugify(
                self.name + " " + secrets.token_hex(2),
                allow_unicode=True,
            )
        return super().save(*args, **kwargs)


class Member(TimeStampedModelMixin):
    class MemberRole(models.TextChoices):
        OWNER = "OWNER", "owner"
        ADMIN = "ADMIN", "admin"
        MEMBER = "MEMBER", "member"

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        verbose_name=_("organization"),
        related_name="organization_members",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("user"),
        related_name="organizations",
    )
    role = models.CharField(
        verbose_name=_("role"),
        max_length=20,
        choices=MemberRole.choices,
        default=MemberRole.MEMBER,
    )
    is_active = models.BooleanField(_("status"), default=True)

    class Meta:
        db_table = "members"
        verbose_name = _("member")
        verbose_name_plural = _("members")

    def __str__(self) -> str:
        return f"{self.org}: {self.user}"


class Invitation(models.Model):
    class InvitationStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACCEPTED = "ACCEPTED", "Accepted"
        EXPIRED = "EXPIRED", "Expired"

    token = models.UUIDField(
        _("invitation token"),
        default=uuid4,
        unique=True,
        editable=False,
    )
    email = models.EmailField(
        _("invitee email"),
    )
    role = models.CharField(
        verbose_name=_("role"),
        max_length=20,
        choices=Member.MemberRole.choices,
        default=Member.MemberRole.MEMBER,
    )
    invited_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("invited by"),
        related_name="invitations",
        db_index=True,
    )
    status = models.CharField(
        _("status"),
        choices=InvitationStatus.choices,
        default=InvitationStatus.PENDING,
        db_index=True,
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="invitations",
        verbose_name=_("organization"),
    )
    expired_at = models.DateTimeField(
        _("expired at"),
        editable=False,
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        db_table = "invitations"
        verbose_name = "invitation"
        verbose_name_plural = "invitations"
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"{self.token!s}"

    def save(self, *args, **kwargs):
        if not self.pk:
            expiry_duration = settings.INVITATION_EXPIRY_MINUTES
            self.expired_at = timezone.now() + relativedelta(minutes=expiry_duration)
        return super().save(*args, **kwargs)

    @property
    def valid(self) -> bool:
        return timezone.now() <= self.expired_at
