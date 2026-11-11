from django.contrib import admin

from .models import Atendimento


@admin.register(Atendimento)
class AtendimentoAdmin(admin.ModelAdmin):
    """Admin usado como interface mínima do projeto na Sprint 1."""

    list_display = ("assunto", "cliente", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("cliente", "assunto")
    readonly_fields = ("created_at", "updated_at")

    def has_delete_permission(self, request, obj=None):
        # RNF08: sem exclusão de atendimento nesta versão.
        return False
