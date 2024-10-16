# Generated by Django 5.1.1 on 2024-10-12 06:45

import django.db.models.deletion
import django_countries.fields
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Organization",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
                (
                    "name",
                    models.CharField(db_index=True, max_length=64, verbose_name="name"),
                ),
                (
                    "slug",
                    models.SlugField(
                        editable=False, max_length=84, unique=True, verbose_name="slug"
                    ),
                ),
                (
                    "avatar",
                    models.ImageField(upload_to="organization/", verbose_name="avatar"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("ACTIVE", "Active"), ("SUSPENDED", "Suspended")],
                        db_index=True,
                        default="ACTIVE",
                        verbose_name="status",
                    ),
                ),
                (
                    "country",
                    django_countries.fields.CountryField(
                        db_index=True, max_length=2, verbose_name="country"
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="owned_organizations",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="owner",
                    ),
                ),
            ],
            options={
                "verbose_name": "organization",
                "verbose_name_plural": "organizations",
                "db_table": "organizations",
                "ordering": ("-id",),
            },
        ),
        migrations.CreateModel(
            name="OrganizationInvitation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "token",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        unique=True,
                        verbose_name="invitation token",
                    ),
                ),
                (
                    "email",
                    models.EmailField(max_length=254, verbose_name="invitee email"),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("OWNER", "owner"),
                            ("ADMIN", "admin"),
                            ("MEMBER", "member"),
                        ],
                        default="MEMBER",
                        max_length=20,
                        verbose_name="role",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "Pending"),
                            ("ACCEPTED", "Accepted"),
                            ("EXPIRED", "Expired"),
                        ],
                        db_index=True,
                        default="PENDING",
                        verbose_name="status",
                    ),
                ),
                (
                    "expired_at",
                    models.DateTimeField(editable=False, verbose_name="expired at"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "invited_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="invitations",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="invited by",
                    ),
                ),
                (
                    "org",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="invitations",
                        to="organization.organization",
                        verbose_name="organization",
                    ),
                ),
            ],
            options={
                "verbose_name": "Organization Invitation",
                "verbose_name_plural": "Organization Invitations",
                "db_table": "org_invitations",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="OrganizationMember",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("OWNER", "owner"),
                            ("ADMIN", "admin"),
                            ("MEMBER", "member"),
                        ],
                        default="MEMBER",
                        max_length=20,
                        verbose_name="role",
                    ),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="status")),
                (
                    "org",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="organization_members",
                        to="organization.organization",
                        verbose_name="organization",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="organizations",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "organization member",
                "verbose_name_plural": "organization members",
                "db_table": "organization_members",
            },
        ),
    ]
