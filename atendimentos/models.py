from django.db import models


class Atendimento(models.Model):
    """Atendimento recebido de um cliente, com status controlado pelo responsável."""

    class Status(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        EM_ANDAMENTO = "em_andamento", "Em andamento"
        CONCLUIDO = "concluido", "Concluído"

    cliente = models.CharField("cliente", max_length=120)
    assunto = models.CharField("assunto", max_length=160)
    descricao = models.TextField("descrição", blank=True)
    status = models.CharField(
        "status",
        max_length=20,
        choices=Status.choices,
        default=Status.PENDENTE,
    )
    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        verbose_name = "atendimento"
        verbose_name_plural = "atendimentos"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.assunto} ({self.cliente})"
