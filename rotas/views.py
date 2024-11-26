from django.shortcuts import render, redirect
from rotas.models import rota
from rotas.forms import CadastrarRota


def cadastrar_rota(request):

    erro = None
    texto = None

    if request.method == "POST":
        form = CadastrarRota(request.POST)
        if form.is_valid():
            form.save()
            return redirect("vertodasrotas")
    else:
        form = rota
        erro = request.GET.get("erro")
        texto = request.GET.get("texto")

    return render(request, 'rotas_cadastrar.html', {"form": form, "erro":erro, "texto":texto})


def ver_rotas(request):
    todas_rotas = rota.objects.all()
    return render(request, 'rotas_lista.html', {'todas_rotas':todas_rotas})
