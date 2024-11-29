import pytest
from armazenamento.models import Produto  

@pytest.mark.django_db
def test_produto_salvamento():
    produto = Produto.objects.create(
        NF="JG4545-jp",
        fornecedor="Bebidas JP",
        cidade="João Pessoa",
        cliente="Carlos",
        origem="João pessoa",
        destino="Campina grande",
        quantidade_total=50
    )

    
    produto_salvo = Produto.objects.get(NF="JG4545-jp")


    assert produto_salvo.NF == "JG4545-jp"
    assert produto_salvo.fornecedor == "Bebidas JP"
    assert produto_salvo.cidade == "João Pessoa"
    assert produto_salvo.cliente == "Carlos"
    assert produto_salvo.origem == "João pessoa"
    assert produto_salvo.destino == "Campina grande"
    assert produto_salvo.quantidade_total == 50
    assert produto_salvo.data_criacao is not None