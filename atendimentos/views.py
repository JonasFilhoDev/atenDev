"""Views do app atendimentos.

Sprint 2 entrega a autenticação e a proteção das páginas. A lista aqui é o mínimo que
permite provar a proteção no navegador: o filtro por status, o cadastro, a edição e as
mensagens de sucesso entram na Sprint 3.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Atendimento


@login_required
def lista(request):
    """Lista os atendimentos do mais recente para o mais antigo."""
    atendimentos = Atendimento.objects.all()
    return render(request, "atendimentos/lista.html", {"atendimentos": atendimentos})
