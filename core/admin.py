from django.contrib import admin
from .models import Pessoa, Grupo, Plano, Servico, PlanoServico

# Cadastro de Pessoa com exibição simples
@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'cpf')
    # Como a relação com Grupo é definida no model Grupo, podemos deixar somente a listagem aqui.

# Cadastro de Grupo com filtro horizontal para facilitar seleção de pessoas e planos
@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    filter_horizontal = ('pessoas', 'planos')  # Interface amigável para selecionar muitas relações

# Inline para a associação de Plano com Serviços (descontos) no admin de Plano
class PlanoServicoInline(admin.TabularInline):
    model = PlanoServico
    extra = 1

@admin.register(Plano)
class PlanoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    inlines = [PlanoServicoInline]

# Cadastro de Serviço com exibição simples
@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'valor')

# Cadastro direto da associação, caso queira gerenciar separadamente
@admin.register(PlanoServico)
class PlanoServicoAdmin(admin.ModelAdmin):
    list_display = ('plano', 'servico', 'desconto')
