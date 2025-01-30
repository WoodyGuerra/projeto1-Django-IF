from django.shortcuts import render, get_object_or_404, redirect
from .models import Aluno, Autor, Livro, Emprestimo
from .forms import AlunoForm, AutorForm, LivroForm, EmprestimoForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User

    
# View de login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('aluno_list')
        else:
            messages.error(request, 'Usuário ou senha inválidos. Tente novamente.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# View de logout
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# View de cadastro de usuário

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso! Faça login.')
            return redirect('login')
        else:
            messages.error(request, 'Erro ao criar conta. Verifique os dados e tente novamente.')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def perfil_usuario(request):
    usuario = request.user

    context = {
        'usuario': usuario
    }

    return render(request, 'perfil_usuario.html', context)

# Aluno Views
@login_required
def aluno_list(request):
    alunos = Aluno.objects.all()
    return render(request, 'aluno_list.html', {'alunos': alunos})

@login_required
def aluno_detail(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    return render(request, 'aluno_detail.html', {'aluno': aluno})

@login_required
def aluno_create(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('aluno_list')
    else:
        form = AlunoForm()
    return render(request, 'aluno_form.html', {'form': form})

@login_required
def aluno_update(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    if request.method == 'POST':
        form = AlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            return redirect('aluno_list')
    else:
        form = AlunoForm(instance=aluno)
    return render(request, 'aluno_update.html', {'form': form})

@login_required
def aluno_delete(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    if request.method == 'POST':
        aluno.delete()
        return redirect('aluno_list')
    return render(request, 'aluno_confirm_delete.html', {'aluno': aluno})

# Autor Views
@login_required
def autor_list(request):
    autores = Autor.objects.all()
    return render(request, 'autor_list.html', {'autores': autores})

@login_required
def autor_create(request):
    if request.method == 'POST':
        form = AutorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('autor_list')
    else:
        form = AutorForm()
    return render(request, 'autor_form.html', {'form': form})

@login_required
def autor_update(request, pk):
    autor = get_object_or_404(Autor, pk=pk)
    if request.method == 'POST':
        form = AutorForm(request.POST, instance=autor)
        if form.is_valid():
            form.save()
            return redirect('autor_list')
    else:
        form = AutorForm(instance=autor)
    return render(request, 'autor_update.html', {'form': form})

@login_required
def autor_delete(request, pk):
    autor = get_object_or_404(Autor, pk=pk)
    if request.method == 'POST':
        autor.delete()
        return redirect('autor_list')
    return render(request, 'autor_confirm_delete.html', {'autor': autor})

# Livro Views
@login_required
def livro_list(request):
    livros = Livro.objects.all()
    return render(request, 'livro_list.html', {'livros': livros})

@login_required
def livro_detail(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    return render(request, 'livro_detail.html', {'livro': livro})

@login_required
def livro_create(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('livro_list')
        else:
            print(form.errors)
    else:
        form = LivroForm()
    return render(request, 'livro_form.html', {'form': form})

@login_required
def livro_update(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        form = LivroForm(request.POST, instance=livro)
        if form.is_valid():
            form.save()
            return redirect('livro_list')
    else:
        form = LivroForm(instance=livro)
    return render(request, 'livro_update.html', {'form': form})

@login_required
def livro_delete(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        livro.delete()
        return redirect('livro_list')
    return render(request, 'livro_confirm_delete.html', {'livro': livro})

# Emprestimo Views
@login_required
def emprestimo_list(request):
    emprestimos = Emprestimo.objects.all()
    return render(request, 'emprestimo_list.html', {'emprestimos': emprestimos})

@login_required
def emprestimo_create(request):
    if request.method == 'POST':
        form = EmprestimoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('emprestimo_list')
    else:
        form = EmprestimoForm()
    return render(request, 'emprestimo_form.html', {'form': form})

@login_required
def emprestimo_update(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    if request.method == 'POST':
        form = EmprestimoForm(request.POST, instance=emprestimo)
        if form.is_valid():
            form.save()
            return redirect('emprestimo_list')
    else:
        form = EmprestimoForm(instance=emprestimo)
    return render(request, 'emprestimo_update.html', {'form': form})

@login_required
def emprestimo_delete(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    if request.method == 'POST':
        emprestimo.delete()
        return redirect('emprestimo_list')
    return render(request, 'emprestimo_confirm_delete.html', {'emprestimo': emprestimo})