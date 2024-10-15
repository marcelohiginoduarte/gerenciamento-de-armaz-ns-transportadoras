from django import forms
from .models import MovimentacaoEstoque, Produto


class ProdutoForms(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['NF', 'fornecedor', 'cidade',]



class MovimentacaoEstoqueForm(forms.ModelForm):
    class Meta:
        model = MovimentacaoEstoque
        fields = ['produto', 'local', 'tipo', 'quantidade', 'observacao']