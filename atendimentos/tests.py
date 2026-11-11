from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Atendimento


class AtendimentoModelTests(TestCase):
    def test_status_padrao_e_pendente(self):
        atendimento = Atendimento.objects.create(
            cliente="Cliente Fictício",
            assunto="Revisar formulário",
        )

        self.assertEqual(atendimento.status, Atendimento.Status.PENDENTE)
        self.assertEqual(atendimento.get_status_display(), "Pendente")

    def test_lista_ordena_do_mais_recente_para_o_mais_antigo(self):
        antigo = Atendimento.objects.create(cliente="Cliente A", assunto="Antigo")
        novo = Atendimento.objects.create(cliente="Cliente B", assunto="Novo")

        self.assertEqual(list(Atendimento.objects.all()), [novo, antigo])

    def test_filtro_por_status_concluido(self):
        Atendimento.objects.create(cliente="Cliente A", assunto="Continua pendente")
        concluido = Atendimento.objects.create(
            cliente="Cliente B",
            assunto="Já concluído",
            status=Atendimento.Status.CONCLUIDO,
        )

        concluidos = Atendimento.objects.filter(status=Atendimento.Status.CONCLUIDO)

        self.assertEqual(list(concluidos), [concluido])

    def test_assunto_vazio_e_rejeitado_na_validacao(self):
        atendimento = Atendimento(cliente="Cliente Fictício", assunto="")

        with self.assertRaises(ValidationError):
            atendimento.full_clean()


class AtendimentoAdminTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="responsavel",
            email="responsavel@example.com",
            password="senha-ficticia-123",
        )
        self.client.force_login(self.user)

    def test_modelo_registrado_no_admin(self):
        self.assertIn(Atendimento, admin.site._registry)

    def test_admin_lista_atendimento_com_filtro_de_status(self):
        Atendimento.objects.create(cliente="Cliente Fictício", assunto="Revisar formulário")

        response = self.client.get(
            reverse("admin:atendimentos_atendimento_changelist")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Revisar formulário")
        self.assertContains(response, "Pendente")

    def test_admin_bloqueia_exclusao(self):
        model_admin = admin.site._registry[Atendimento]
        request = self.client.request().wsgi_request
        request.user = self.user

        self.assertFalse(model_admin.has_delete_permission(request))
