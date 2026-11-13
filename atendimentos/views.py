"""Views do app atendimentos.

Sprint 3: lista com filtro por status, cadastro e edição com mensagem de sucesso. Toda
tela de atendimento passa por `login_required`, como manda o RF01.
Sprint 5: cadastro e edição exigem permissão do Django, e quem só consulta recebe um aviso
na lista. É o que permite o usuário de demonstração sem criar nem alterar registro.
"""

from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AtendimentoForm
from .models import Atendimento


def requer_permissao(permissao):
    """Deixa passar quem tem a permissão; os demais voltam à lista com aviso."""

    def decorador(view):
        @wraps(view)
        def envolvida(request, *args, **kwargs):
            if request.user.has_perm(permissao):
                return view(request, *args, **kwargs)
            messages.warning(
                request,
                "Usuário de demonstração: cadastrar e editar estão bloqueados. "
                "A lista e o filtro continuam disponíveis.",
            )
            return redirect("atendimentos:lista")

        return envolvida

    return decorador


def _status_valido(valor):
    """Aceita apenas um valor que exista em Atendimento.Status."""
    return valor in Atendimento.Status.values


@login_required
def lista(request):
    """Lista os atendimentos do mais recente para o mais antigo, com filtro por status."""
    status_escolhido = request.GET.get("status", "").strip()
    if not _status_valido(status_escolhido):
        status_escolhido = ""

    atendimentos = Atendimento.objects.all()
    if status_escolhido:
        atendimentos = atendimentos.filter(status=status_escolhido)

    contexto = {
        "atendimentos": atendimentos,
        "status_escolhido": status_escolhido,
        "status_rotulo": dict(Atendimento.Status.choices).get(status_escolhido, ""),
        "filtros": Atendimento.Status.choices,
    }
    return render(request, "atendimentos/lista.html", contexto)


@login_required
@requer_permissao("atendimentos.add_atendimento")
def criar(request):
    """Cadastra um atendimento; o status começa como pendente se não for escolhido."""
    if request.method == "POST":
        form = AtendimentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Atendimento cadastrado.")
            return redirect("atendimentos:lista")
    else:
        form = AtendimentoForm()

    return render(
        request,
        "atendimentos/form.html",
        {"form": form, "titulo": "Novo atendimento"},
    )


@login_required
@requer_permissao("atendimentos.change_atendimento")
def editar(request, pk):
    """Edita qualquer campo de um atendimento, inclusive o status."""
    atendimento = get_object_or_404(Atendimento, pk=pk)

    if request.method == "POST":
        form = AtendimentoForm(request.POST, instance=atendimento)
        if form.is_valid():
            form.save()
            messages.success(request, "Atendimento atualizado.")
            return redirect("atendimentos:lista")
    else:
        form = AtendimentoForm(instance=atendimento)

    return render(
        request,
        "atendimentos/form.html",
        {"form": form, "titulo": "Editar atendimento", "atendimento": atendimento},
    )
