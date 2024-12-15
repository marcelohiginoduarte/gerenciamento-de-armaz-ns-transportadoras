from django.db import models
from django.utils import timezone


class Produto(models.Model):
    status_carga = [('aguardando','aguardando Transpor'),
                    ('em_transito','Em Transito'),
                    ('entregue','Entregue'),
                    ]


    NF = models.CharField(max_length=100)
    fornecedor = models.CharField(max_length=50, unique=True)
    cidade = models.CharField(max_length=50, unique=False)
    cliente = models.CharField(max_length=50, blank=True, null=True)
    origem = models.CharField(max_length=1362, blank=True, null=True)
    destino = models.CharField(max_length=1362, blank=True, null=True)
    quantidade_total = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=25, choices=status_carga, blank=True, null=True, default='aguardando')
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.NF


class LocalArmazenamento(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome


class MovimentacaoEstoque(models.Model):

    TIPO_MOVIMENTACAO = [("ENTRADA", "Entrada"), ("SAIDA", "Saída")]

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    local = models.ForeignKey(LocalArmazenamento, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=7, choices=TIPO_MOVIMENTACAO)
    quantidade = models.PositiveIntegerField()
    data_movimentacao = models.DateTimeField(auto_now_add=True)
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tipo} - {self.produto.nome}"

    def save(self, *args, **kwargs):
        if self.tipo == "ENTRADA":
            self.produto.quantidade_total += self.quantidade
            espaco = EspacoArmazenamento.objects.filter(produto__isnull=True).first()
            if espaco:
                espaco.produto = self.produto
                espaco.save()
        elif self.tipo == "SAIDA":
            if self.produto.quantidade_total >= self.quantidade:
                self.produto.quantidade_total -= self.quantidade
                espaco = EspacoArmazenamento.objects.filter(
                    produto=self.produto
                ).first()
                if espaco:
                    espaco.produto = None
                    espaco.save()
            else:
                raise ValueError("Quantidade insuficiente em estoque para saída.")

        self.produto.save()
        super().save(*args, **kwargs)


class EspacoArmazenamento(models.Model):
    numero = models.PositiveBigIntegerField(unique=True)
    produto = models.ForeignKey(
        Produto, null=True, blank=True, on_delete=models.SET_NULL
    )
    vaga = models.BooleanField(default=True)

    def __str__(self):
        return f'Espaço {self.numero} - {"Ocupado" if not self.vaga else "Vago"}'
    
    def incluir_produto(self, produto):
        if not self.vaga:
            raise ValueError("Esta vaga ja está ocupada")
        self.produto = produto
        self.vaga = False
        self.save()

class RegistroEntrega(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    espaco = models.ForeignKey(EspacoArmazenamento, on_delete=models.CASCADE)
    data_entrega = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Registro de {self.produto.nome} - {self.espaco.numero} - {self.data_entrega}"
    
capitais_brasileiras = [
    {"capital": "Rio Branco", "estado": "AC", "latitude": -9.97499, "longitude": -67.8243},
    {"capital": "Maceió", "estado": "AL", "latitude": -9.66599, "longitude": -35.735},
    {"capital": "Macapá", "estado": "AP", "latitude": 0.0355, "longitude": -51.0705},
    {"capital": "Manaus", "estado": "AM", "latitude": -3.10194, "longitude": -60.025},
    {"capital": "Salvador", "estado": "BA", "latitude": -12.9714, "longitude": -38.5014},
    {"capital": "Fortaleza", "estado": "CE", "latitude": -3.71722, "longitude": -38.5433},
    {"capital": "Brasília", "estado": "DF", "latitude": -15.7942, "longitude": -47.8822},
    {"capital": "Vitória", "estado": "ES", "latitude": -20.3155, "longitude": -40.3128},
    {"capital": "Goiânia", "estado": "GO", "latitude": -16.6864, "longitude": -49.2643},
    {"capital": "São Luís", "estado": "MA", "latitude": -2.53874, "longitude": -44.2825},
    {"capital": "Belo Horizonte", "estado": "MG", "latitude": -19.9191, "longitude": -43.9386},
    {"capital": "Campo Grande", "estado": "MS", "latitude": -20.4697, "longitude": -54.6201},
    {"capital": "Cuiabá", "estado": "MT", "latitude": -15.6014, "longitude": -56.0979},
    {"capital": "Belém", "estado": "PA", "latitude": -1.45502, "longitude": -48.5044},
    {"capital": "João Pessoa", "estado": "PB", "latitude": -7.11509, "longitude": -34.8641},
    {"capital": "Curitiba", "estado": "PR", "latitude": -25.4284, "longitude": -49.2733},
    {"capital": "Recife", "estado": "PE", "latitude": -8.04756, "longitude": -34.877},
    {"capital": "Teresina", "estado": "PI", "latitude": -5.09194, "longitude": -42.8034},
    {"capital": "Rio de Janeiro", "estado": "RJ", "latitude": -22.9068, "longitude": -43.1729},
    {"capital": "Natal", "estado": "RN", "latitude": -5.79448, "longitude": -35.211},
    {"capital": "Porto Alegre", "estado": "RS", "latitude": -30.0346, "longitude": -51.2177},
    {"capital": "Porto Velho", "estado": "RO", "latitude": -8.76077, "longitude": -63.8999},
    {"capital": "Boa Vista", "estado": "RR", "latitude": 2.82384, "longitude": -60.6753},
    {"capital": "Florianópolis", "estado": "SC", "latitude": -27.5954, "longitude": -48.548},
    {"capital": "São Paulo", "estado": "SP", "latitude": -23.5505, "longitude": -46.6333},
    {"capital": "Aracaju", "estado": "SE", "latitude": -10.9472, "longitude": -37.0731},
    {"capital": "Palmas", "estado": "TO", "latitude": -10.2491, "longitude": -48.3243},
]


