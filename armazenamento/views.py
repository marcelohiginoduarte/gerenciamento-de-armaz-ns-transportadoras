from django.shortcuts import render, redirect
from .models import Produto
from .forms import ProdutoForms


def home(request):
    return render(request, 'home.html')

def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'Produto_estoque.html', {'produtos':produtos})

def Castrar_produtos(request):

    erro = None
    texto = None

    if request.method == 'POST':
        form = ProdutoForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listarprodutos')
    else:
        form = Produto
        erro = request.GET.get('erro')
        texto = request.GET.get('texto')

    return render(request, 'Produto_criar.html', {'form':form, 'erro':erro, 'texto':texto})

