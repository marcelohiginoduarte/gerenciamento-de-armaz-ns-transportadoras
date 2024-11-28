from django.db import models
from armazenamento.models import Produto
import openrouteservice
from decouple import config

client = openrouteservice.Client(key=config('Chave_api'))

client = openrouteservice.Client(key='SUA_API_KEY')

class rota(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.DO_NOTHING)
    origem = models.CharField(max_length=255)
    destino = models.CharField(max_length=255)
    distancia = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Em quilômetros
    tempo_estimado = models.DurationField(blank=True, null=True)  # Exemplo: timedelta
    custo_estimado = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.origem} → {self.destino}"
    
    def save(self, *args, **kwargs):
        if not self.distancia or not self.tempo_estimado:
            self.calcular_rota()
        super().save(*args, **kwargs)

    def calcular_rota(self):
        try:
            # Geocodificação para obter coordenadas
            origem_resposta = client.pelias_search(self.origem)
            destino_resposta = client.pelias_search(self.destino)

            if not origem_resposta['features'] or not destino_resposta['features']:
                raise ValueError("Origem ou destino não encontrados.")

            origem_coords = origem_resposta['features'][0]['geometry']['coordinates']
            destino_coords = destino_resposta['features'][0]['geometry']['coordinates']

            # Solicitação de rota
            rota = client.directions(
                coordinates=[origem_coords, destino_coords],
                profile='driving-car',
                format='geojson'
            )

            # Extração de distância e duração
            distancia_km = rota['features'][0]['properties']['segments'][0]['distance'] / 1000
            duracao_segundos = rota['features'][0]['properties']['segments'][0]['duration']

            # Verificação de distância
            if distancia_km is None or distancia_km == 0:
                raise ValueError("A distância não pode ser nula ou zero.")

            # Conversão de segundos para timedelta
            duracao_timedelta = timedelta(seconds=duracao_segundos)

            # Atualização dos campos
            self.distancia = distancia_km
            self.tempo_estimado = duracao_timedelta
            self.custo_estimado = distancia_km * 2.5
            self.save()

        except Exception as e:
            print(f"Erro ao calcular a rota: {e}")


class Viagem(models.Model):
    rota = models.ForeignKey(rota, on_delete=models.DO_NOTHING)
    carga = models.ForeignKey(Produto, on_delete=models.DO_NOTHING)
    data_partida = models.DateTimeField()
    data_chegada = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Viagem de {self.rota.origem} para {self.rota.destino} com {self.carga}"
