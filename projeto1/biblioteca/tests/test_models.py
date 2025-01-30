from django.test import TestCase
from django.core.exceptions import ValidationError
from biblioteca.models import Aluno, Autor, Livro, Escrito, Emprestimo
from datetime import date


class AlunoModelTest(TestCase):
    def test_cpf_deve_conter_apenas_numeros(self):
        aluno = Aluno(nome="João Silva", cpf="123456789a1", email="joao@email.com", telefone="87999999999")
        with self.assertRaises(ValidationError) as context:
            aluno.full_clean()
        self.assertIn("CPF deve conter apenas números", str(context.exception))

    def test_cpf_deve_ter_11_digitos(self):
        aluno = Aluno(nome="Maria Souza", cpf="123456789", email="maria@email.com", telefone="87999999999")
        with self.assertRaises(ValidationError) as context:
            aluno.full_clean()
        self.assertIn("CPF deve ter 11 dígitos", str(context.exception))

    def test_telefone_deve_conter_apenas_numeros(self):
        aluno = Aluno(nome="Carlos Mendes", cpf="12345678901", email="carlos@email.com", telefone="fone123456")
        with self.assertRaises(ValidationError) as context:
            aluno.full_clean()
        self.assertIn("Telefone deve conter apenas números", str(context.exception))

class AutorModelTest(TestCase):
    def test_nome_autor_deve_ser_unico(self):
        Autor.objects.create(nome="Machado de Assis")
        autor_duplicado = Autor(nome="Machado de Assis")
        with self.assertRaises(ValidationError):
            autor_duplicado.full_clean()

class LivroModelTest(TestCase):
    def test_isbn_deve_ser_unico(self):
        Livro.objects.create(isbn="9781234567897", titulo="Dom Casmurro", situacao="Disponível")
        livro_duplicado = Livro(isbn="9781234567897", titulo="Memórias Póstumas", situacao="Disponível")
        with self.assertRaises(ValidationError):
            livro_duplicado.full_clean()

class EmprestimoModelTest(TestCase):
    def setUp(self):
        self.aluno = Aluno.objects.create(nome="Pedro Oliveira", cpf="12345678901", email="pedro@email.com", telefone="81999999999")
        self.autor = Autor.objects.create(nome="José de Alencar")
        self.livro = Livro.objects.create(isbn="9786543210987", titulo="Iracema", situacao="Disponível")
        self.livro.autores.add(self.autor)

    def test_nao_pode_emprestar_livro_ja_emprestado(self):
        Emprestimo.objects.create(aluno=self.aluno, livro=self.livro)
        emprestimo_novo = Emprestimo(aluno=self.aluno, livro=self.livro)

        with self.assertRaises(ValidationError) as context:
            emprestimo_novo.full_clean()
        self.assertIn("Livro já está emprestado.", str(context.exception))

    def test_data_devolucao_nao_pode_ser_anterior_ao_emprestimo(self):
        emprestimo = Emprestimo(aluno=self.aluno, livro=self.livro)
        emprestimo.data_emprestimo = date(2023, 1, 5)  # Definindo a data de empréstimo
        emprestimo.data_devolucao = date(2023, 1, 1)  # Data de devolução anterior

        with self.assertRaises(ValidationError) as context:
            emprestimo.full_clean()
        
        self.assertIn("Data de devolução deve ser posterior à data de empréstimo.", str(context.exception))

    def test_emprestimo_muda_situacao_do_livro_para_emprestado(self):
        emprestimo = Emprestimo.objects.create(aluno=self.aluno, livro=self.livro)
        self.livro.refresh_from_db()
        self.assertEqual(self.livro.situacao, "Emprestado")

