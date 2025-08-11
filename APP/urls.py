from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('cadastrar-veiculo/', views.cadastrar_veiculo, name='cadastrar_veiculo'),
    path('cadastrar-gr/', views.cadastrar_gr, name='cadastrar_gr'),
    path('cadastrar-checklist/', views.cadastrar_checklist, name='cadastrar_checklist'),
    path('logout/', views.user_logout, name='logout'),
    path('veiculo/<int:pk>/', views.veiculo_detalhes, name='veiculo_detalhes'),
    path('excluir-veiculo/<int:pk>/', views.excluir_veiculo, name='excluir_veiculo'),
]