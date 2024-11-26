from django.db import models
from armazenamento.models import Produto
import openrouteservice
from decouple import config

client = openrouteservice.Client(key=config('Chave_api'))

class rota(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.DO_NOTHING)
    origem = models.CharField(max_length=255)
    destino = models.CharField(max_length=255)
    distancia = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Em quilômetros
    tempo_estimado = models.DurationField(blank=True, null=True)  # Exemplo: 2h 30m
    custo_estimado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.origem} → {self.destino}"

    def calcular_rota(self):
    
        origem_resposta = client.pelias_search(self.origem)
        destino_resposta = client.pelias_search(self.destino)

        
        if not origem_resposta['features'] or not destino_resposta['features']:
            print("Erro: Dados de origem ou destino não encontrados")
            return

        
        origem_coords = origem_resposta['features'][0]['geometry']['coordinates']
        destino_coords = destino_resposta['features'][0]['geometry']['coordinates']

        
        print("Origem:", origem_coords)
        print("Destino:", destino_coords)

        
        rota = client.directions(
            coordinates=[origem_coords, destino_coords],
            profile='driving-car',
            format='geojson'
        )

        
        print("Rota:", rota)

        
        distancia = rota['features'][0]['properties']['segments'][0]['distance'] / 1000  # em km
        tempo_estimado_segundos = rota['features'][0]['properties']['segments'][0]['duration']
        tempo_estimado = str(tempo_estimado_segundos // 3600) + 'h ' + str((tempo_estimado_segundos % 3600) // 60) + 'm'

        
        if distancia is None or distancia == 0:
            raise ValueError("A distância não pode ser nula ou zero")

        
        self.distancia = distancia
        self.tempo_estimado = tempo_estimado
        self.custo_estimado = self.distancia * 2.5
        self.save()


class Viagem(models.Model):
    rota = models.ForeignKey(rota, on_delete=models.DO_NOTHING)
    carga = models.ForeignKey(Produto, on_delete=models.DO_NOTHING)
    data_partida = models.DateTimeField()
    data_chegada = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Viagem de {self.rota.origem} para {self.rota.destino} com {self.carga}"
