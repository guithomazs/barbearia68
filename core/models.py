from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from decimal import Decimal

class Pessoa(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=14, unique=True)

    def __str__(self):
        return self.nome

class Grupo(models.Model):
    nome = models.CharField(max_length=100)
    # Relação muitos-para-muitos entre Pessoa e Grupo:
    pessoas = models.ManyToManyField(Pessoa, related_name='grupos', blank=True)
    # Um grupo pode estar associado a vários planos:
    planos = models.ManyToManyField('Plano', related_name='grupos', blank=True)

    def __str__(self):
        return self.nome

class Plano(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    # Aqui não definimos um campo "valor" porque, conforme dito,
    # o valor (desconto) será definido para cada serviço no contexto do plano.

    def __str__(self):
        return self.nome

class ServicoProduto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    eh_produto = models.BooleanField(default=False, verbose_name="É Produto?")

    class Meta:
        verbose_name = "Serviço ou Produto"
        verbose_name_plural = "Serviços e Produtos"

    def __str__(self):
        tipo = "Produto" if self.eh_produto else "Serviço"
        return f"{self.nome} ({tipo})"
class PlanoServico(models.Model):
    plano = models.ForeignKey(Plano, related_name='plano_servicos', on_delete=models.CASCADE)
    servico = models.ForeignKey(ServicoProduto, related_name='plano_servicos', on_delete=models.CASCADE)
    # Desconto representado em porcentagem para este serviço dentro do plano.
    desconto = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        help_text="Percentual de desconto para o serviço neste plano"
    )
    
    class Meta:
        unique_together = ('plano', 'servico')  # Garante uma associação única para cada par plano/serviço

    def __str__(self):
        return f"{self.plano.nome} - {self.servico.nome}: {self.desconto}%"
    
class Caixa(models.Model):
    TIPO_CHOICES = (
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    )

    descricao = models.CharField(max_length=200)
    
    # Relacionamento genérico para a origem (apenas Pessoa e Grupo serão permitidos)
    origin_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Tipo de Origem"
    )
    origin_object_id = models.PositiveIntegerField(null=True, blank=True)
    origem = GenericForeignKey('origin_content_type', 'origin_object_id')
    
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=7, choices=TIPO_CHOICES)
    data = models.DateTimeField(default=timezone.now)

    @property
    def valor_formatado(self):
        sinal = "-" if self.tipo == "saida" else ""
        return f"{sinal}R$ {abs(self.valor):.2f}"

    def __str__(self):
        origem_str = str(self.origem) if self.origem else "Sem origem"
        return f"{self.get_tipo_display()} - {self.descricao} ({self.valor_formatado}) - Origem: {origem_str}"
