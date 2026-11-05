from django.contrib import admin

from .models import Conteudo, Menu


@admin.register(Conteudo)
class ConteudoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "slug", "ativo")
    list_editable = ("ativo",)
    list_filter = ("ativo",)
    search_fields = ("titulo", "slug")
    # Preenche o slug automaticamente enquanto o título é digitado.
    prepopulated_fields = {"slug": ("titulo",)}


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("titulo", "tipo_destino", "ordem", "ativo", "destino")
    # Permite mudar a ordem e ativar/desativar direto na lista.
    list_editable = ("ordem", "ativo")
    list_filter = ("tipo_destino", "ativo")
    search_fields = ("titulo",)
    ordering = ("ordem", "titulo")

    @admin.display(description="destino")
    def destino(self, item):
        if item.tipo_destino == Menu.TIPO_EXTERNO:
            return item.url_externa
        return item.conteudo
