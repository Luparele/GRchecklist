from django.contrib import admin
from .models import GerenciadoraDeRisco, Veiculo, Checklist

@admin.register(GerenciadoraDeRisco)
class GerenciadoraDeRiscoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'regra_validade')
    search_fields = ('nome',)

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'modalidade', 'data_cadastro')
    search_fields = ('placa',)
    list_filter = ('modalidade',)

@admin.register(Checklist)
class ChecklistAdmin(admin.ModelAdmin):
    list_display = ('veiculo', 'gerenciadora', 'data_emissao', 'dias_para_vencer')
    list_filter = ('gerenciadora', 'veiculo')
    autocomplete_fields = ('veiculo', 'gerenciadora')