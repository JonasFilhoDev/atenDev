"""Views do app atendimentos.

Sprint 3: lista com filtro por status, cadastro e edição com mensagem de sucesso. Toda
tela de atendimento passa por `login_required`, como manda o RF01.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AtendimentoForm
from .models import Atendimento


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
