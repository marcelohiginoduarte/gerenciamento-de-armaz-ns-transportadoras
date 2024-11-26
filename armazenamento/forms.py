from django import forms
from .models import MovimentacaoEstoque, Produto, EspacoArmazenamento


class ProdutoForms(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ["NF", "fornecedor", "cliente", "origem", "destino","cidade", "quantidade_total"]


class MovimentacaoEstoqueForm(forms.ModelForm):
    class Meta:
        model = MovimentacaoEstoque
        fields = ["produto", "local", "tipo", "quantidade", "observacao"]


class EspacoArmazenamentoForm(forms.ModelForm):
    class Meta:
        model = EspacoArmazenamento
        fields = ["numero", "produto", "vaga"]

class SalvarProdutoNoEspacaoForm(forms.ModelForm):
    class Meta:
        model = EspacoArmazenamento
        fields = ['produto']