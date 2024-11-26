from django import forms
from rotas.models import rota, Viagem

class CadastrarRota(forms.ModelForm):
    class Meta:
        model = rota
        fields = ['produto',
                'origem',
                'destino',
                'distancia',
                'tempo_estimado',
                'custo_estimado'
                ]


class CadastrarViagem(forms.ModelForm):
    class Meta:
        model = Viagem
        fields = ['rota',
                'carga',
                'data_partida',
                'data_chegada'
                ]