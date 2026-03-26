from django.contrib import admin

from .models import Acesso, Link


class AuditoriaModelAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")

    def save_model(self, request, obj, form, change):
        obj.save(user=request.user)


@admin.register(Link)
class LinkAdmin(AuditoriaModelAdmin):
    list_display = ("desc", "link", "thumbnail_url", "created_at", "updated_by")
    search_fields = ("desc", "link")
    list_filter = ("created_by", "updated_by")


@admin.register(Acesso)
class AcessoAdmin(AuditoriaModelAdmin):
    list_display = ("group", "link", "created_at", "updated_by")
    search_fields = ("group__name", "link__desc")
    list_filter = ("group", "link")
