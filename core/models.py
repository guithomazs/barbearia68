from django.db import models

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

class Servico(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome

class PlanoServico(models.Model):
    plano = models.ForeignKey(Plano, related_name='plano_servicos', on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, related_name='plano_servicos', on_delete=models.CASCADE)
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
