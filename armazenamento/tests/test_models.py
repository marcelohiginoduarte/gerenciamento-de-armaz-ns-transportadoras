import pytest
from django.test import TestCase
from armazenamento.models import Produto
from django.db.utils import IntegrityError

@pytest.mark.django_db
def test_savalmento_bd():
    produto = Produto.objects.create(
        NF="TGjktr1123",
        fornecedor = "Fornecedortest",
        cidade="Carpina",
        cliente="Douglas",
        origem="Recife",
        destino="Carpina",
        quantidade_total=80
    )

    assert produto.NF == "TGjktr1123"
    assert produto.fornecedor == "Fornecedortest"
    assert produto.cidade == "Carpina"
    assert produto.cliente == "Douglas"
    assert produto.origem == "Recife"
    assert produto.destino == "Carpina"
    assert produto.quantidade_total == 80

@pytest.mark.django_db
def test_fornecedor_unico():
    Produto.objects.create(
        NF="123456",
        fornecedor="Fornecedor X",
        cidade="Cidade Y"
    )
    with pytest.raises(IntegrityError):
        Produto.objects.create(
            NF="789012",
            fornecedor="Fornecedor X",
            cidade="Outra Cidade"
        )

@pytest.mark.django_db
def test_valores_padrao():
    produto = Produto.objects.create(
        NF="123456",
        fornecedor="Fornecedor X",
        cidade="Cidade Y"
    )
    assert produto.quantidade_total == 0
    assert produto.cliente is None
    assert produto.origem is None
    assert produto.destino is None

@pytest.mark.django_db
def test_representacao_em_string():
    produto = Produto.objects.create(
        NF="654321",
        fornecedor="Fornecedor Y",
        cidade="Cidade Z"
    )
    assert str(produto) == "654321"
