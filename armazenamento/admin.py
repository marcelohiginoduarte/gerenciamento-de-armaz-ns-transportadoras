from django.contrib import admin
from .models import Produto, EspacoArmazenamento


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('NF', 'fornecedor', 'cidade')
    list_display_links = ('NF',)

admin.site.register(Produto, ProdutoAdmin)      

class EspacoArmazenamentoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'produto')
    list_display_links = ('numero',)

admin.site.register(EspacoArmazenamento, EspacoArmazenamentoAdmin)
