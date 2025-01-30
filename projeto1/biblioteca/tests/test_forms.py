from django.test import TestCase
from biblioteca.forms import AlunoForm, AutorForm, LivroForm, EmprestimoForm
from biblioteca.models import Aluno, Autor, Livro, Emprestimo
from datetime import date

class AlunoFormTest(TestCase):
    def test_aluno_form_valid_data(self):
        form = AlunoForm(data={"nome": "João Silva", "cpf": "12345678901", "email": "joao@email.com", "telefone": "81999999999"})
        self.assertTrue(form.is_valid())

    def test_aluno_form_invalid_data(self):
        form = AlunoForm(data={"nome": "", "cpf": "abc", "email": "email_invalido", "telefone": "123"})
        print("Erros do AlunoForm:", form.errors)  
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), len(form.errors.keys()))  

class AutorFormTest(TestCase):
    def test_autor_form_valid_data(self):
        form = AutorForm(data={"nome": "Machado de Assis"})
        self.assertTrue(form.is_valid())

    def test_autor_form_invalid_data(self):
        form = AutorForm(data={"nome": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("nome", form.errors)

class LivroFormTest(TestCase):
    def test_livro_form_valid_data(self):
        autor = Autor.objects.create(nome="J. K. Rowling")
        form = LivroForm(data={"isbn": "9783161484100", "titulo": "Harry Potter", "situacao": "Disponível", "autores": [autor.id]})
        self.assertTrue(form.is_valid())

    def test_livro_form_invalid_data(self):
        form = LivroForm(data={"isbn": "", "titulo": "", "situacao": "Indisponível", "autores": []})
        print("Erros do LivroForm:", form.errors) 
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), len(form.errors.keys()))

class EmprestimoFormTest(TestCase):
    def setUp(self):
        self.aluno = Aluno.objects.create(nome="Carlos Souza", cpf="12345678901", email="carlos@email.com", telefone="81999999999")
        self.autor = Autor.objects.create(nome="Isaac Asimov")
        self.livro = Livro.objects.create(isbn="9783161484101", titulo="Fundação", situacao="Disponível")
        self.livro.autores.add(self.autor)

    def test_emprestimo_form_valid_data(self):
        form = EmprestimoForm(data={"aluno": self.aluno.id, "livro": self.livro.id, "data_devolucao": date.today()})
        self.assertTrue(form.is_valid())

    
    def test_emprestimo_form_invalid_data(self):
        form = EmprestimoForm(data={"aluno": self.aluno.id, "livro": self.livro.id, "data_devolucao": "invalid_date"})
        print("Erros do EmprestimoForm:", form.errors) 
        self.assertFalse(form.is_valid())
        self.assertIn("data_devolucao", form.errors)
