from django.shortcuts import render

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Pessoa, Grupo, Plano, Servico, PlanoServico

from decimal import Decimal


def home(request):
    return render(request, 'core/verificar.html')

# ----- Views para Pessoa -----
class PessoaListView(ListView):
    model = Pessoa
    template_name = 'core/pessoa_list.html'
    context_object_name = 'pessoas'

class PessoaDetailView(DetailView):
    model = Pessoa
    template_name = 'core/pessoa_detail.html'
    context_object_name = 'pessoa'

class PessoaCreateView(CreateView):
    model = Pessoa
    template_name = 'core/pessoa_form.html'
    fields = ['nome', 'telefone', 'email', 'cpf']
    success_url = reverse_lazy('pessoa_list')

class PessoaUpdateView(UpdateView):
    model = Pessoa
    template_name = 'core/pessoa_form.html'
    fields = ['nome', 'telefone', 'email', 'cpf']
    success_url = reverse_lazy('pessoa_list')

class PessoaDeleteView(DeleteView):
    model = Pessoa
    template_name = 'core/pessoa_confirm_delete.html'
    success_url = reverse_lazy('pessoa_list')


# ----- Views para Grupo -----
class GrupoListView(ListView):
    model = Grupo
    template_name = 'core/grupo_list.html'
    context_object_name = 'grupos'

class GrupoDetailView(DetailView):
    model = Grupo
    template_name = 'core/grupo_detail.html'
    context_object_name = 'grupo'

class GrupoCreateView(CreateView):
    model = Grupo
    template_name = 'core/grupo_form.html'
    fields = ['nome', 'pessoas', 'planos']
    success_url = reverse_lazy('grupo_list')

class GrupoUpdateView(UpdateView):
    model = Grupo
    template_name = 'core/grupo_form.html'
    fields = ['nome', 'pessoas', 'planos']
    success_url = reverse_lazy('grupo_list')

class GrupoDeleteView(DeleteView):
    model = Grupo
    template_name = 'core/grupo_confirm_delete.html'
    success_url = reverse_lazy('grupo_list')


# ----- Views para Plano -----
class PlanoListView(ListView):
    model = Plano
    template_name = 'core/plano_list.html'
    context_object_name = 'planos'

class PlanoDetailView(DetailView):
    model = Plano
    template_name = 'core/plano_detail.html'
    context_object_name = 'plano'

class PlanoCreateView(CreateView):
    model = Plano
    template_name = 'core/plano_form.html'
    fields = ['nome', 'descricao']
    success_url = reverse_lazy('plano_list')

class PlanoUpdateView(UpdateView):
    model = Plano
    template_name = 'core/plano_form.html'
    fields = ['nome', 'descricao']
    success_url = reverse_lazy('plano_list')

class PlanoDeleteView(DeleteView):
    model = Plano
    template_name = 'core/plano_confirm_delete.html'
    success_url = reverse_lazy('plano_list')


# ----- Views para Serviço -----
class ServicoListView(ListView):
    model = Servico
    template_name = 'core/servico_list.html'
    context_object_name = 'servicos'

class ServicoDetailView(DetailView):
    model = Servico
    template_name = 'core/servico_detail.html'
    context_object_name = 'servico'

class ServicoCreateView(CreateView):
    model = Servico
    template_name = 'core/servico_form.html'
    fields = ['nome', 'descricao', 'valor']
    success_url = reverse_lazy('servico_list')

class ServicoUpdateView(UpdateView):
    model = Servico
    template_name = 'core/servico_form.html'
    fields = ['nome', 'descricao', 'valor']
    success_url = reverse_lazy('servico_list')

class ServicoDeleteView(DeleteView):
    model = Servico
    template_name = 'core/servico_confirm_delete.html'
    success_url = reverse_lazy('servico_list')


# ----- Views para PlanoServico (Associação com desconto) -----
class PlanoServicoListView(ListView):
    model = PlanoServico
    template_name = 'core/planoservico_list.html'
    context_object_name = 'planoservicos'

class PlanoServicoDetailView(DetailView):
    model = PlanoServico
    template_name = 'core/planoservico_detail.html'
    context_object_name = 'planoservico'

class PlanoServicoCreateView(CreateView):
    model = PlanoServico
    template_name = 'core/planoservico_form.html'
    fields = ['plano', 'servico', 'desconto']
    success_url = reverse_lazy('planoservico_list')

class PlanoServicoUpdateView(UpdateView):
    model = PlanoServico
    template_name = 'core/planoservico_form.html'
    fields = ['plano', 'servico', 'desconto']
    success_url = reverse_lazy('planoservico_list')

class PlanoServicoDeleteView(DeleteView):
    model = PlanoServico
    template_name = 'core/planoservico_confirm_delete.html'
    success_url = reverse_lazy('planoservico_list')


def verificar_servicos(request):
    resultado = None
    erro = None

    if request.method == 'POST':
        busca = request.POST.get('busca')
        pessoa = Pessoa.objects.filter(cpf=busca).first() or Pessoa.objects.filter(nome__icontains=busca).first()

        if not pessoa:
            erro = "Pessoa não encontrada."
        else:
            grupos = pessoa.grupos.all()
            planos = set()
            for grupo in grupos:
                planos.update(grupo.planos.all())

            # Pega todos os serviços do sistema
            todos_servicos = Servico.objects.all()
            servico_descontos = {}

            for servico in todos_servicos:
                maior_desconto = Decimal('0')
                for plano in planos:
                    ps = plano.plano_servicos.filter(servico=servico).first()
                    if ps and ps.desconto > maior_desconto:
                        maior_desconto = ps.desconto

                valor_com_desconto = servico.valor * (Decimal('1') - maior_desconto / Decimal('100'))
                servico_descontos[servico.id] = {
                    'servico': servico,
                    'desconto': maior_desconto,
                    'valor_com_desconto': valor_com_desconto
                }

            resultado = list(servico_descontos.values())

    return render(request, 'core/verificar.html', {
        'resultado': resultado,
        'erro': erro
    })
