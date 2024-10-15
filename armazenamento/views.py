from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto, EspacoArmazenamento, RegistroEntrega
from .forms import ProdutoForms
from django.utils import timezone


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

def lista_espacos(request):
    espacos = EspacoArmazenamento.objects.all()
    return render(request, 'armazenamento_espaco.html', {'espacos': espacos})


def saida_para_entrega(request, espaco_id):
    espaco = get_object_or_404(EspacoArmazenamento, id=espaco_id)
    
    if espaco.produto:
        # Cria o registro da saída sem usar numero_estoque
        RegistroEntrega.objects.create(
            produto=espaco.produto,
            espaco=espaco,
            data_entrega=timezone.now(),
        )
        
        # Limpa o produto do espaço e o número
        espaco.produto = None
        espaco.numero = None  # Limpa o número ou redefine conforme necessário
        espaco.save()
        
        return redirect('pagina_de_confirmacao')  # Redireciona para uma página de confirmação
    
    return HttpResponse("O espaço já está vago.")

def sua_view_de_confirmacao(request):
    return render(request, 'nome_do_template_de_confirmacao.html')
