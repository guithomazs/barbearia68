from django.urls import path
from .views import (
    PessoaListView, PessoaDetailView, PessoaCreateView, PessoaUpdateView, PessoaDeleteView,
    GrupoListView, GrupoDetailView, GrupoCreateView, GrupoUpdateView, GrupoDeleteView,
    PlanoListView, PlanoDetailView, PlanoCreateView, PlanoUpdateView, PlanoDeleteView,
    ServicoListView, ServicoDetailView, ServicoCreateView, ServicoUpdateView, ServicoDeleteView,
    PlanoServicoListView, PlanoServicoDetailView, PlanoServicoCreateView, PlanoServicoUpdateView, PlanoServicoDeleteView, home, verificar_servicos
)

urlpatterns = [
    
    path('', home, name='home'),
    
    # Rotas para Pessoa
    path('pessoas/', PessoaListView.as_view(), name='pessoa_list'),
    path('pessoas/<int:pk>/', PessoaDetailView.as_view(), name='pessoa_detail'),
    path('pessoas/criar/', PessoaCreateView.as_view(), name='pessoa_create'),
    path('pessoas/<int:pk>/editar/', PessoaUpdateView.as_view(), name='pessoa_update'),
    path('pessoas/<int:pk>/excluir/', PessoaDeleteView.as_view(), name='pessoa_delete'),

    # Rotas para Grupo
    path('grupos/', GrupoListView.as_view(), name='grupo_list'),
    path('grupos/<int:pk>/', GrupoDetailView.as_view(), name='grupo_detail'),
    path('grupos/criar/', GrupoCreateView.as_view(), name='grupo_create'),
    path('grupos/<int:pk>/editar/', GrupoUpdateView.as_view(), name='grupo_update'),
    path('grupos/<int:pk>/excluir/', GrupoDeleteView.as_view(), name='grupo_delete'),

    # Rotas para Plano
    path('planos/', PlanoListView.as_view(), name='plano_list'),
    path('planos/<int:pk>/', PlanoDetailView.as_view(), name='plano_detail'),
    path('planos/criar/', PlanoCreateView.as_view(), name='plano_create'),
    path('planos/<int:pk>/editar/', PlanoUpdateView.as_view(), name='plano_update'),
    path('planos/<int:pk>/excluir/', PlanoDeleteView.as_view(), name='plano_delete'),

    # Rotas para Serviço
    path('servicos/', ServicoListView.as_view(), name='servico_list'),
    path('servicos/<int:pk>/', ServicoDetailView.as_view(), name='servico_detail'),
    path('servicos/criar/', ServicoCreateView.as_view(), name='servico_create'),
    path('servicos/<int:pk>/editar/', ServicoUpdateView.as_view(), name='servico_update'),
    path('servicos/<int:pk>/excluir/', ServicoDeleteView.as_view(), name='servico_delete'),

    # Rotas para PlanoServico
    path('planoservicos/', PlanoServicoListView.as_view(), name='planoservico_list'),
    path('planoservicos/<int:pk>/', PlanoServicoDetailView.as_view(), name='planoservico_detail'),
    path('planoservicos/criar/', PlanoServicoCreateView.as_view(), name='planoservico_create'),
    path('planoservicos/<int:pk>/editar/', PlanoServicoUpdateView.as_view(), name='planoservico_update'),
    path('planoservicos/<int:pk>/excluir/', PlanoServicoDeleteView.as_view(), name='planoservico_delete'),
    
    path('verificar/', verificar_servicos, name='verificar'),

]
