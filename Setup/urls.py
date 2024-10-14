from django.contrib import admin
from django.urls import path
from armazenamento.views import lista_produtos, Castrar_produtos, home


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('listarprodutos', lista_produtos, name='listarprodutos'),
    path('criarproduto', Castrar_produtos, name='cadastrarproduto'),
    
]
