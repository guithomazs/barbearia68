from django.shortcuts import render, redirect

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Pessoa, Grupo, Plano, ServicoProduto, PlanoServico, Caixa
from .forms import CaixaForm

from django.db.models import Sum, Case, When, F, DecimalField
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType

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
    model = ServicoProduto
    template_name = 'core/servico_list.html'
    context_object_name = 'servicos'

class ServicoDetailView(DetailView):
    model = ServicoProduto
    template_name = 'core/servico_detail.html'
    context_object_name = 'servico'

class ServicoCreateView(CreateView):
    model = ServicoProduto
    template_name = 'core/servico_form.html'
    fields = ['nome', 'descricao', 'valor']
    success_url = reverse_lazy('servico_list')

class ServicoUpdateView(UpdateView):
    model = ServicoProduto
    template_name = 'core/servico_form.html'
    fields = ['nome', 'descricao', 'valor']
    success_url = reverse_lazy('servico_list')

class ServicoDeleteView(DeleteView):
    model = ServicoProduto
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
    pessoa = None
    grupos = []
    planos_utilizados = set()

    if request.method == 'POST':
        busca = request.POST.get('busca')
        pessoa = Pessoa.objects.filter(cpf=busca).first() or Pessoa.objects.filter(nome__icontains=busca).first()

        todos_servicos = ServicoProduto.objects.all()
        servico_descontos = {}

        if not pessoa:
            erro = "Pessoa não encontrada."
        else:
            grupos = pessoa.grupos.all()
            planos = set()
            for grupo in grupos:
                planos.update(grupo.planos.all())

            for servico in todos_servicos:
                maior_desconto = Decimal('0')
                plano_usado = None
                for plano in planos:
                    ps = plano.plano_servicos.filter(servico=servico).first()
                    if ps and ps.desconto > maior_desconto:
                        maior_desconto = ps.desconto
                        plano_usado = plano
                valor_com_desconto = servico.valor * (Decimal('1') - maior_desconto / Decimal('100'))
                servico_descontos[servico.id] = {
                    'servico': servico,
                    'desconto': maior_desconto,
                    'valor_com_desconto': valor_com_desconto,
                    'plano_usado': plano_usado
                }

                if plano_usado:
                    planos_utilizados.add(plano_usado)

        # Caso a pessoa não seja encontrada, mostrar os serviços com 0% de desconto
        if not pessoa:
            for servico in todos_servicos:
                servico_descontos[servico.id] = {
                    'servico': servico,
                    'desconto': Decimal('0'),
                    'valor_com_desconto': servico.valor,
                    'plano_usado': None
                }

        resultado = list(servico_descontos.values())

    return render(request, 'core/verificar.html', {
        'resultado': resultado,
        'erro': erro,
        'pessoa': pessoa,
        'grupos': grupos,
        'planos_utilizados': planos_utilizados,
        'busca': request.POST.get('busca', '')
    })
    
def fluxo_caixa(request):
    if request.method == "POST":
        form = CaixaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fluxo_caixa')
    else:
        form = CaixaForm()

    registros = Caixa.objects.all().order_by('-data')

    saldo = Caixa.objects.aggregate(
        total=Sum(
            Case(
                When(tipo='entrada', then=F('valor')),
                When(tipo='saida', then=-F('valor')),
                output_field=DecimalField()
            )
        )
    )['total'] or Decimal('0.00')

    context = {
        'registros': registros,
        'saldo': saldo,
        'form': form,
    }
    return render(request, 'core/fluxo_caixa.html', context)

def listar_origem(request):
    ct_id = request.GET.get('ct_id')
    try:
        ct_id = int(ct_id)
        content_type = ContentType.objects.get_for_id(ct_id)
        model_label = content_type.model
        if model_label == 'pessoa':
            objetos = Pessoa.objects.all().values('id', 'nome')
        elif model_label == 'grupo':
            objetos = Grupo.objects.all().values('id', 'nome')
        else:
            objetos = []
        return JsonResponse(list(objetos), safe=False)
    except (ValueError, ContentType.DoesNotExist):
        return JsonResponse([], safe=False)
    