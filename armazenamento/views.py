from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto, EspacoArmazenamento, RegistroEntrega
from .forms import ProdutoForms
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.conf import settings
from datetime import datetime



def home(request):
    return render(request, 'home.html')

def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'Produto_estoque.html', {'produtos':produtos})

def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    if request.method == 'POST':
        form = ProdutoForms(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('listarprodutos')
    
    else:
        form = ProdutoForms(instance=produto)
    return render(request, 'editar_produto.html', {'form':form})


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

@method_decorator(csrf_exempt, name='dispatch')
class CadastrarProdutoAPI(View):
    def post(self, request):
        # Verificar a chave da API no cabeçalho
        api_key = request.headers.get('Authorization')
        if api_key != settings.API_SECRET_KEY:
            return JsonResponse({'erro': 'Chave de API inválida.'}, status=403)

        try:
            cadastro = json.loads(request.body)

            NF = cadastro.get('NF')
            fornecedor = cadastro.get('fornecedor')
            cidade = cadastro.get('cidade')
            cliente = cadastro.get('cliente')
            quantidade_total = cadastro.get('quantidade_total')
            data_criacao = cadastro.get('data_criacao')

            if not NF or not fornecedor or not cliente:
                return JsonResponse({'erro': 'NF, fornecedor e cliente são obrigatórios.'}, status=400)

            # Validar data
            try:
                data_criacao = datetime.strptime(data_criacao, '%Y-%m-%d').date() if data_criacao else None
            except ValueError:
                return JsonResponse({'erro': 'Formato de data inválido. Use YYYY-MM-DD.'}, status=400)

            # Criar o produto
            produto = Produto.objects.create(
                NF=NF,
                fornecedor=fornecedor,
                cidade=cidade,
                cliente=cliente,
                quantidade_total=quantidade_total,
                data_criacao=data_criacao
            )
            return JsonResponse({'message': 'Produto cadastrado com sucesso!', 'id': produto.id}, status=201)

        except Exception as e:
            return JsonResponse({'erro': f'Erro interno: {str(e)}'}, status=500)

def lista_espacos(request):
    espacos = EspacoArmazenamento.objects.all()
    produtos = Produto.objects.all()

    if request.method == "POST":
        produto_id = request.POST.get('produto_id')
        if produto_id:
            produto = get_object_or_404(Produto, id=produto_id)

            for espaco in espacos:
                if espaco.vaga:  
                    espaco.produto = produto
                    espaco.vaga = False 
                    espaco.save()  
                    return redirect('espaçoarmazenamento')  

            return HttpResponse("Todos os espaços estão ocupados.")  

        return HttpResponse("Nenhum produto selecionado.")

    return render(request, 'armazenamento_espaco.html', {'espacos': espacos, 'produtos': produtos})


def saida_para_entrega(request, espaco_id):
    espaco = get_object_or_404(EspacoArmazenamento, id=espaco_id)
    
    if espaco.produto:
        RegistroEntrega.objects.create(
            produto=espaco.produto,
            espaco=espaco,
            data_entrega=timezone.now(),
        )
        
        
        espaco.produto = None
        espaco.vago = True  
        espaco.save()
        
        return redirect('pagina_de_confirmacao')
    
    return HttpResponse("O espaço já está vago.")

def sua_view_de_confirmacao(request):
    return render(request, 'nome_do_template_de_confirmacao.html')

def incluir_produto(request, espaco_id):
    espaco = get_object_or_404(EspacoArmazenamento, id=espaco_id)
    
    
    produtos = Produto.objects.all()


    if request.method == "POST":
        produto_id = request.POST.get('produto_id')
        if produto_id:
            produto = get_object_or_404(Produto, id=produto_id)
            
            if espaco.vaga:
                espaco.produto = produto
                espaco.vaga = False
                espaco.save()
                return redirect('pagina_de_confirmacao')  
            else:
                return HttpResponse("O espaço já está ocupado.")
        else:
            return HttpResponse("Nenhum produto selecionado.")
    
    
    return render(request, 'incluir_produto.html', {'espaco': espaco, 'produtos': produtos})

