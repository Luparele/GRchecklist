from django.db import models
from django.utils import timezone

class GerenciadoraDeRisco(models.Model):
    """
    Modelo para a Gerenciadora de Risco (GR).
    """
    class ValidadeChecklist(models.TextChoices):
        NO_EMBARQUE = '01', 'No Embarque'
        TRINTA_DIAS = '30', '30 Dias'
        SESSENTA_DIAS = '60', '60 Dias'
        NOVENTA_DIAS = '90', '90 Dias'

    nome = models.CharField(max_length=200, unique=True, verbose_name="Nome da GR")
    regra_validade = models.CharField(
        max_length=2,
        choices=ValidadeChecklist.choices,
        default=ValidadeChecklist.NO_EMBARQUE,
        verbose_name="Validade do Checklist"
    )

    def __str__(self):
        return self.nome

class Veiculo(models.Model):
    """
    Modelo para os veículos da transportadora.
    """
    class Modalidade(models.TextChoices):
        FROTA = 'FROTA', 'Frota'
        AGREGADO = 'AGREGADO', 'Agregado'
        TERCEIRO = 'TERCEIRO', 'Terceiro'

    placa = models.CharField(max_length=7, unique=True, verbose_name="Placa")
    modalidade = models.CharField(
        max_length=10,
        choices=Modalidade.choices,
        default=Modalidade.FROTA,
        verbose_name="Modalidade"
    )
    crlv = models.FileField(upload_to='crlv/', blank=True, null=True, verbose_name="Upload CRLV")
    ficha_ativacao_omnilink = models.FileField(upload_to='fichas/', blank=True, null=True, verbose_name="Ficha de Ativação Omnilink")
    data_cadastro = models.DateTimeField(default=timezone.now, verbose_name="Data de Cadastro")

    def __str__(self):
        return self.placa

class Checklist(models.Model):
    """
    Modelo para os checklists de rastreamento de veículos.
    """
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    gerenciadora = models.ForeignKey(GerenciadoraDeRisco, on_delete=models.CASCADE)
    aprovado = models.BooleanField(default=True, verbose_name="Aprovado")
    causa_reprovacao = models.TextField(blank=True, null=True, verbose_name="Causa da Reprovação")
    data_emissao = models.DateField(default=timezone.now, verbose_name="Data de Emissão")

    def __str__(self):
        return f"Checklist {self.veiculo.placa} - {self.gerenciadora.nome}"

    @property
    def data_vencimento(self):
        """Calcula a data de vencimento com base na regra da GR."""
        if self.gerenciadora.regra_validade == '01':
            return self.data_emissao
        
        dias = int(self.gerenciadora.regra_validade)
        return self.data_emissao + timezone.timedelta(days=dias)

    @property
    def dias_para_vencer(self):
        """Calcula os dias que faltam para o vencimento."""
        hoje = timezone.now().date()
        vencimento = self.data_vencimento
        delta = vencimento - hoje
        return delta.days