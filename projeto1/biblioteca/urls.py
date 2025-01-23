from django.urls import path
from . import views

urlpatterns = [
    
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    
    path('', views.aluno_list, name='aluno_list'),
    
    
    
    path('aluno/<int:pk>/', views.aluno_detail, name='aluno_detail'),
    path('aluno/novo/', views.aluno_create, name='aluno_create'),
    path('aluno/editar/<int:pk>/', views.aluno_update, name='aluno_update'),
    path('aluno/excluir/<int:pk>/', views.aluno_delete, name='aluno_delete'),
    
    path('autor/', views.autor_list, name='autor_list'),
    path('autor/novo/', views.autor_create, name='autor_create'),
    path('autor/editar/<int:pk>/', views.autor_update, name='autor_update'),
    path('autor/excluir/<int:pk>/', views.autor_delete, name='autor_delete'),

    path('livro/', views.livro_list, name='livro_list'),
    path('livro/<int:pk>/', views.livro_detail, name='livro_detail'),
    path('livro/novo/', views.livro_create, name='livro_create'),
    path('livro/editar/<int:pk>/', views.livro_update, name='livro_update'),
    path('livro/excluir/<int:pk>/', views.livro_delete, name='livro_delete'),

    path('emprestimo/', views.emprestimo_list, name='emprestimo_list'),
    path('emprestimo/novo/', views.emprestimo_create, name='emprestimo_create'),
    path('emprestimo/editar/<int:pk>/', views.emprestimo_update, name='emprestimo_update'),
    path('emprestimo/excluir/<int:pk>/', views.emprestimo_delete, name='emprestimo_delete'),
]