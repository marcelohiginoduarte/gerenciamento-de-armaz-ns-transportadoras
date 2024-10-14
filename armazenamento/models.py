from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=True)
    descricao = models.TextField(blank=True, null=True)
    quantidade_total = models.PositiveIntegerField(default=0)
    data_criacao = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.nome
    

class LocalArmazenamento(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome
    

class MovimentacaoEstoque(models.Model):

    TIPO_MOVIMENTACAO = [
        ('ENTRADA', 'Entrada'),
        ('SAIDA', 'Saída')
    ]


    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    local = models.ForeignKey(LocalArmazenamento, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=7, choices=TIPO_MOVIMENTACAO)
    quantidade = models.PositiveIntegerField()
    data_movimentacao = models.DateTimeField(auto_now_add=True)
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.tipo} - {self.produto.nome}'
    
    def save(self, *args, **kwargs):
        if self.tipo == 'ENTRADA':
            self.produto.quantidade_total += self.quantidade
            espaco = EspacoArmazenamento.objects.filter(produto__isnull=True).first()
            if espaco:
                espaco.produto = self.produto
                espaco.save()
        elif self.tipo == 'SAIDA':
            if self.produto.quantidade_total >= self.quantidade:
                self.produto.quantidade_total -= self.quantidade
                espaco = EspacoArmazenamento.objects.filter(produto=self.produto).first()
                if espaco:
                    espaco.produto = None
                    espaco.save()
            else:
                raise ValueError("Quantidade insuficiente em estoque para saída.")
    
        self.produto.save()
        super().save(*args, **kwargs)


class EspacoArmazenamento(models.Model):
    numero = models.PositiveBigIntegerField(unique=True)
    produto = models.ForeignKey(Produto, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'Espaço {self.numero} - {"Ocupado" if self.produto else "Vago"}'