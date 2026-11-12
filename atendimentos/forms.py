"""Formulário de atendimento, com validação no servidor.

Cliente e assunto são obrigatórios porque o modelo não usa `blank=True`; o Django já
devolve a mensagem em português por causa do `LANGUAGE_CODE = 'pt-br'`.
"""

from django import forms

from .models import Atendimento


class AtendimentoForm(forms.ModelForm):
    class Meta:
        model = Atendimento
        fields = ["cliente", "assunto", "descricao", "status"]
        widgets = {
            "cliente": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nome do cliente"}
            ),
            "assunto": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "O que o cliente pediu"}
            ),
            "descricao": forms.Textarea(
                attrs={"class": "form-control", "rows": 4, "placeholder": "Detalhes (opcional)"}
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["descricao"].required = False
