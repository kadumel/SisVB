from django.db import models
from django.contrib.auth.models import User, Group


class AuditoriaSaveMixin:
    """Preenche created_by / updated_by quando save(user=...) for chamado."""

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
        user=None,
    ):
        if user is not None:
            if self._state.adding:
                self.created_by = user
            self.updated_by = user
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )


class Link(AuditoriaSaveMixin, models.Model):
    desc = models.CharField(max_length=40, default="")
    link = models.CharField(max_length=400)
    thumbnail_url = models.CharField(
        max_length=500,
        blank=True,
        default="",
        help_text="URL de uma imagem de capa do painel. Se vazio, usa iframe de pré-visualização.",
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        related_name="links_created",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        related_name="links_updated",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Link"

    def __str__(self):
        return "{}".format(self.desc)


class Acesso(AuditoriaSaveMixin, models.Model):
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    link = models.ForeignKey(Link, on_delete=models.PROTECT)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        related_name="acessos_created",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        related_name="acessos_updated",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Acesso"
        ordering = ["group__name"]

    def __str__(self):
        return f"{self.group.name} - {self.link.desc}"
