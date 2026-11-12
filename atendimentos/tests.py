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


class LoginTests(TestCase):
    """Sprint 2: login, logout e proteção das páginas de atendimento."""

    def setUp(self):
        self.senha = "senha-ficticia-123"
        self.user = get_user_model().objects.create_user(
            username="responsavel",
            password=self.senha,
        )
        self.lista_url = reverse("atendimentos:lista")
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")

    def test_anonimo_e_redirecionado_para_o_login(self):
        response = self.client.get(self.lista_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["Location"], f"{self.login_url}?next={self.lista_url}"
        )

    def test_autenticado_acessa_a_lista(self):
        self.client.force_login(self.user)

        response = self.client.get(self.lista_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "atendimentos/lista.html")

    def test_lista_mostra_responsavel_e_botao_sair(self):
        self.client.force_login(self.user)

        response = self.client.get(self.lista_url)

        self.assertContains(response, "responsavel")
        self.assertContains(response, "Sair")

    def test_pagina_de_login_abre_com_formulario(self):
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="password"')

    def test_credencial_invalida_mostra_erro(self):
        response = self.client.post(
            self.login_url,
            {"username": "responsavel", "password": "senha-errada"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_login_valido_redireciona_para_a_lista(self):
        response = self.client.post(
            self.login_url,
            {"username": "responsavel", "password": self.senha},
        )

        self.assertRedirects(response, self.lista_url)

    def test_logout_encerra_a_sessao(self):
        self.client.force_login(self.user)

        response = self.client.post(self.logout_url)

        self.assertRedirects(response, self.login_url)
        self.assertNotIn("_auth_user_id", self.client.session)

        resposta_da_lista = self.client.get(self.lista_url)
        self.assertEqual(resposta_da_lista.status_code, 302)
        self.assertEqual(
            resposta_da_lista["Location"], f"{self.login_url}?next={self.lista_url}"
        )

    def test_raiz_redireciona_para_a_lista_protegida(self):
        response = self.client.get(reverse("home"))

        self.assertRedirects(response, self.lista_url, fetch_redirect_response=False)

        self.client.force_login(self.user)
        response = self.client.get(reverse("home"))
        self.assertRedirects(response, self.lista_url)


class AtendimentoTelasTests(TestCase):
    """Sprint 3: lista com filtro, cadastro, edição e mensagem de sucesso."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="responsavel",
            password="senha-ficticia-123",
        )
        self.client.force_login(self.user)
        self.lista_url = reverse("atendimentos:lista")
        self.criar_url = reverse("atendimentos:criar")

    def test_anonimo_nao_acessa_cadastro_nem_edicao(self):
        atendimento = Atendimento.objects.create(cliente="Cliente A", assunto="Existente")

        editar_url = reverse("atendimentos:editar", args=[atendimento.pk])
        self.client.logout()

        for url in (self.criar_url, editar_url):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response["Location"].startswith(reverse("login")))

    def test_cadastro_valido_cria_com_status_pendente_e_avisa(self):
        response = self.client.post(
            self.criar_url,
            {
                "cliente": "Cliente Fictício",
                "assunto": "Revisar formulário de contato",
                "descricao": "",
                "status": Atendimento.Status.PENDENTE,
            },
            follow=True,
        )

        self.assertRedirects(response, self.lista_url)
        self.assertContains(response, "Atendimento cadastrado.")

        atendimento = Atendimento.objects.get()
        self.assertEqual(atendimento.status, Atendimento.Status.PENDENTE)
        self.assertEqual(atendimento.assunto, "Revisar formulário de contato")

    def test_assunto_vazio_e_rejeitado_sem_criar(self):
        response = self.client.post(
            self.criar_url,
            {"cliente": "Cliente Fictício", "assunto": "", "status": Atendimento.Status.PENDENTE},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Atendimento.objects.count(), 0)
        self.assertIn("assunto", response.context["form"].errors)
        self.assertContains(response, "Este campo é obrigatório.")

    def test_cliente_vazio_e_rejeitado_sem_criar(self):
        response = self.client.post(
            self.criar_url,
            {"cliente": "   ", "assunto": "Assunto válido", "status": Atendimento.Status.PENDENTE},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Atendimento.objects.count(), 0)
        self.assertIn("cliente", response.context["form"].errors)

    def test_edicao_altera_status_e_persiste(self):
        atendimento = Atendimento.objects.create(
            cliente="Cliente Fictício",
            assunto="Revisar formulário",
        )
        editar_url = reverse("atendimentos:editar", args=[atendimento.pk])

        response = self.client.post(
            editar_url,
            {
                "cliente": atendimento.cliente,
                "assunto": atendimento.assunto,
                "descricao": "",
                "status": Atendimento.Status.CONCLUIDO,
            },
            follow=True,
        )

        self.assertRedirects(response, self.lista_url)
        self.assertContains(response, "Atendimento atualizado.")

        atendimento.refresh_from_db()
        self.assertEqual(atendimento.status, Atendimento.Status.CONCLUIDO)

        lista = self.client.get(self.lista_url)
        self.assertContains(lista, "Concluído")

    def test_filtro_concluido_mostra_apenas_concluidos(self):
        Atendimento.objects.create(cliente="Cliente A", assunto="Continua pendente")
        Atendimento.objects.create(
            cliente="Cliente B",
            assunto="Terminado",
            status=Atendimento.Status.CONCLUIDO,
        )

        response = self.client.get(self.lista_url, {"status": Atendimento.Status.CONCLUIDO})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Terminado")
        self.assertNotContains(response, "Continua pendente")
        self.assertEqual(response.context["status_escolhido"], Atendimento.Status.CONCLUIDO)

    def test_filtro_invalido_mostra_todos(self):
        Atendimento.objects.create(cliente="Cliente A", assunto="Continua pendente")
        Atendimento.objects.create(
            cliente="Cliente B",
            assunto="Terminado",
            status=Atendimento.Status.CONCLUIDO,
        )

        response = self.client.get(self.lista_url, {"status": "inexistente"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Continua pendente")
        self.assertContains(response, "Terminado")
        self.assertEqual(response.context["status_escolhido"], "")

    def test_estado_vazio_do_filtro_explica_o_motivo(self):
        response = self.client.get(self.lista_url, {"status": Atendimento.Status.CONCLUIDO})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nenhum atendimento com o status")

    def test_lista_oferece_caminho_para_cadastrar(self):
        response = self.client.get(self.lista_url)

        self.assertContains(response, self.criar_url)

    def test_edicao_de_atendimento_inexistente_devolve_404(self):
        response = self.client.get(reverse("atendimentos:editar", args=[999999]))

        self.assertEqual(response.status_code, 404)
