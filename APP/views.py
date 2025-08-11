from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Max
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from .models import Veiculo, GerenciadoraDeRisco, Checklist
from .forms import VeiculoForm, GerenciadoraDeRiscoForm, ChecklistForm

def dashboard(request):
    veiculos = Veiculo.objects.all()
    gerenciadoras = GerenciadoraDeRisco.objects.all()
    
    status_checklists = {}
    
    for veiculo in veiculos:
        status_checklists[veiculo.placa] = {}
        for gr in gerenciadoras:
            checklist_recente = Checklist.objects.filter(
                veiculo=veiculo,
                gerenciadora=gr
            ).order_by('-data_emissao').first()
            
            status_checklists[veiculo.placa][gr.nome] = checklist_recente

    tabela_dados = []
    checklists_vencidos = 0
    checklists_a_vencer = 0

    for veiculo in veiculos:
        linha_veiculo = {'id': veiculo.id, 'placa': veiculo.placa, 'modalidade': veiculo.modalidade, 'status_grs': {}}
        for gr in gerenciadoras:
            checklist_recente = status_checklists[veiculo.placa][gr.nome]

            status_celula = 'N/A'
            dias_restantes = None
            causa_reprovacao = None
            
            if checklist_recente:
                if not checklist_recente.aprovado:
                    status_celula = 'REPROVADO'
                    causa_reprovacao = checklist_recente.causa_reprovacao
                else:
                    dias_restantes = checklist_recente.dias_para_vencer
                    if dias_restantes < 0:
                        status_celula = 'VENCIDO'
                        checklists_vencidos += 1
                    elif 0 <= dias_restantes <= 10:
                        status_celula = f'{dias_restantes} dias'
                        checklists_a_vencer += 1
                    elif 11 <= dias_restantes <= 20:
                        status_celula = f'{dias_restantes} dias'
                    else:
                        status_celula = f'{dias_restantes} dias'
            
            linha_veiculo['status_grs'][gr.nome] = {
                'dias': dias_restantes,
                'status_texto': status_celula,
                'causa_reprovacao': causa_reprovacao
            }
        tabela_dados.append(linha_veiculo)
        
    context = {
        'tabela_dados': tabela_dados,
        'gerenciadoras': gerenciadoras,
        'checklists_vencidos': checklists_vencidos,
        'checklists_a_vencer': checklists_a_vencer,
        'veiculo_form': VeiculoForm(),
        'gr_form': GerenciadoraDeRiscoForm(),
        'checklist_form': ChecklistForm(),
        'login_form': AuthenticationForm(),
    }
    return render(request, 'APP/dashboard.html', context)

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                    return JsonResponse({'success': True})
                else:
                    return redirect('dashboard')
    
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse({'success': False, 'message': 'Usuário ou senha inválidos.'}, status=400)
    else:
        return redirect('dashboard')

def user_logout(request):
    logout(request)
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    else:
        return redirect('dashboard')

@login_required
@require_POST
def cadastrar_veiculo(request):
    placa = request.POST.get('placa')
    form = VeiculoForm(request.POST, request.FILES)

    veiculo_existente = Veiculo.objects.filter(placa=placa).first()
    
    if veiculo_existente:
        veiculo_existente.modalidade = request.POST.get('modalidade')
        if request.FILES.get('crlv'):
            veiculo_existente.crlv = request.FILES.get('crlv')
        if request.FILES.get('ficha_ativacao_omnilink'):
            veiculo_existente.ficha_ativacao_omnilink = request.FILES.get('ficha_ativacao_omnilink')
        veiculo_existente.save()
        message = f'Veículo com placa {placa} atualizado com sucesso!'
        return JsonResponse({'success': True, 'message': message})
    else:
        if form.is_valid():
            form.save()
            message = 'Veículo cadastrado com sucesso!'
            return JsonResponse({'success': True, 'message': message})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

@login_required
@require_POST
def cadastrar_gr(request):
    nome = request.POST.get('nome')
    form = GerenciadoraDeRiscoForm(request.POST)

    gr_existente = GerenciadoraDeRisco.objects.filter(nome=nome).first()
    
    if gr_existente:
        gr_existente.regra_validade = request.POST.get('regra_validade')
        gr_existente.save()
        message = f'Gerenciadora de Risco "{nome}" atualizada com sucesso!'
        return JsonResponse({'success': True, 'message': message})
    else:
        if form.is_valid():
            form.save()
            message = 'Gerenciadora de Risco cadastrada com sucesso!'
            return JsonResponse({'success': True, 'message': message})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

@login_required
@require_POST
def cadastrar_checklist(request):
    form = ChecklistForm(request.POST)
    if form.is_valid():
        veiculo = form.cleaned_data.get('veiculo')
        gerenciadora = form.cleaned_data.get('gerenciadora')
        data_emissao = form.cleaned_data.get('data_emissao')
        aprovado = form.cleaned_data.get('aprovado')
        causa_reprovacao = form.cleaned_data.get('causa_reprovacao')

        checklist_existente = Checklist.objects.filter(
            veiculo=veiculo,
            gerenciadora=gerenciadora
        ).first()

        if checklist_existente:
            checklist_existente.data_emissao = data_emissao
            checklist_existente.aprovado = aprovado
            checklist_existente.causa_reprovacao = causa_reprovacao
            checklist_existente.save()
            message = f'Checklist do veículo {veiculo.placa} para {gerenciadora.nome} atualizado com sucesso!'
        else:
            form.save()
            message = 'Checklist cadastrado com sucesso!'
        
        return JsonResponse({'success': True, 'message': message})
    else:
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

@login_required
@require_POST
def excluir_veiculo(request, pk):
    veiculo = get_object_or_404(Veiculo, pk=pk)
    veiculo.delete()
    return JsonResponse({'success': True, 'message': 'Veículo excluído com sucesso!'})

@login_required
def veiculo_detalhes(request, pk):
    veiculo = get_object_or_404(Veiculo, pk=pk)
    checklists_historico = Checklist.objects.filter(veiculo=veiculo).order_by('-data_emissao')
    
    context = {
        'veiculo': veiculo,
        'checklists_historico': checklists_historico,
    }
    return render(request, 'APP/veiculo_detalhes.html', context)