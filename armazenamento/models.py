from django.db import models
from django.utils import timezone


class Produto(models.Model):
    NF = models.CharField(max_length=100)
    fornecedor = models.CharField(max_length=50, unique=True)
    cidade = models.CharField(max_length=50, unique=False)
    cliente = models.CharField(max_length=50, blank=True, null=True)
    quantidade_total = models.PositiveIntegerField(default=0)
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
