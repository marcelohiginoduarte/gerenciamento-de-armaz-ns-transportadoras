from django.contrib import admin
from django.urls import path
from armazenamento.views import (
    lista_produtos,
    Castrar_produtos,
    home,
    lista_espacos,
    entrada_produto_armazem,
    saida_para_entrega,
    sua_view_de_confirmacao,
    incluir_produto,
    editar_produto,
    criar_espaco_armazenamento,
    exibir_quantidade_produto,
    CadastrarProdutoAPI,
)
from rotas.views import cadastrar_rota, ver_rotas


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("listarprodutos", lista_produtos, name="listarprodutos"),
    path("criarproduto", Castrar_produtos, name="cadastrarproduto"),
    path("editarproduto/<int:produto_id>", editar_produto, name="editarproduto"),
    path("api/produtos", CadastrarProdutoAPI.as_view(), name="cadastrarprodutoviaapi"),
    path("armazenamento/espaco", lista_espacos, name="espaçoarmazenamento"),
    path("entradaproutoarmazen/<int:espaco_id>/", entrada_produto_armazem, name='entrada_espaco_armazenamento'),
    path(
        "saida_para_entrega/<int:espaco_id>/",
        saida_para_entrega,
        name="saida_para_entrega",
    ),
    path('armazenamento/criarespaco', criar_espaco_armazenamento, name='criarespacoarmazenamento'),
    path(
        "pagina-de-confirmacao/", sua_view_de_confirmacao, name="pagina_de_confirmacao"
    ),
    path('quantidadeproduto', exibir_quantidade_produto, name='quantidadeproduto'),
    path(
        "incluir_produto/<int:espaco_id>/<int:produto_id>/",
        incluir_produto,
        name="incluir_produto",
    ),
    path("rotas/cadastrar_rota", cadastrar_rota, name='cadastrarrotas'),
    path("rotas/todasrotas", ver_rotas, name='vertodasrotas'),
]
