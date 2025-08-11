from django import forms
from .models import Veiculo, GerenciadoraDeRisco, Checklist

class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['placa', 'modalidade', 'crlv', 'ficha_ativacao_omnilink']
        widgets = {
            'placa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: ABC1234'}),
            'modalidade': forms.Select(attrs={'class': 'form-control'}),
        }

class GerenciadoraDeRiscoForm(forms.ModelForm):
    class Meta:
        model = GerenciadoraDeRisco
        fields = ['nome', 'regra_validade']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Gerenciadora S.A.'}),
            'regra_validade': forms.Select(attrs={'class': 'form-control'}),
        }

class ChecklistForm(forms.ModelForm):
    class Meta:
        model = Checklist
        fields = ['veiculo', 'gerenciadora', 'aprovado', 'causa_reprovacao', 'data_emissao']
        widgets = {
            'veiculo': forms.Select(attrs={'class': 'form-control'}),
            'gerenciadora': forms.Select(attrs={'class': 'form-control'}),
            'aprovado': forms.Select(choices=[(True, 'Sim'), (False, 'Não')], attrs={'class': 'form-control'}),
            'causa_reprovacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'data_emissao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }