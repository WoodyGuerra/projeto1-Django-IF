from django import forms
from .models import Aluno, Autor, Livro, Emprestimo

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'cpf', 'email', 'telefone']

class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nome']

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['isbn', 'titulo', 'situacao', 'autores']

class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['aluno', 'livro', 'data_devolucao']

    def save(self, commit=True):
        emprestimo = super().save(commit=False)
        emprestimo.livro.situacao = "Emprestado"
        if commit:
            emprestimo.livro.save()
            emprestimo.save()
        return emprestimo