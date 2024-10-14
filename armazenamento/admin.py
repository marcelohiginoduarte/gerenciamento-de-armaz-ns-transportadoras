from django.contrib import admin
from .models import Produto


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sku', 'descricao')
    list_display_links = ('nome',)

admin.site.register(Produto, ProdutoAdmin)      
