from django.contrib import admin
from django.urls import path
from armazenamento.views import lista_produtos, Castrar_produtos, home, lista_espacos, saida_para_entrega


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('listarprodutos', lista_produtos, name='listarprodutos'),
    path('criarproduto', Castrar_produtos, name='cadastrarproduto'),

    path('armazenamento/espaco', lista_espacos, name='espaçoarmazenamento'),
    path('saida_para_entrega/<int:espaco_id>/', saida_para_entrega, name='saida_para_entrega'),
    
]
