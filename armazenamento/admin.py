from django.contrib import admin
from .models import Produto


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('NF', 'fornecedor', 'cidade')
    list_display_links = ('NF',)

admin.site.register(Produto, ProdutoAdmin)      
