from django.db import models
from django.core.exceptions import ValidationError
    
class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11)
    email = models.EmailField(max_length=254)
    telefone = models.CharField(max_length=11)
    
    def clean(self):
        if not isinstance(self.cpf, str) or not self.cpf.isdigit():
            raise ValidationError('CPF deve conter apenas números')
        if not isinstance(self.telefone, str) or not self.telefone.isdigit():
            raise ValidationError('Telefone deve conter apenas números')
        if len(self.cpf) != 11:
            raise ValidationError('CPF deve ter 11 dígitos')
        super().clean()
        
    def __str__(self):
        return self.nome

class Autor(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class Livro(models.Model):
    isbn = models.CharField(max_length=13, unique=True)
    titulo = models.CharField(max_length=150)
    situacao = models.CharField(max_length=50, choices=[("Disponível", "Disponível"), ("Emprestado", "Emprestado")])
    autores = models.ManyToManyField(Autor, through="Escrito")

    def __str__(self):
        return self.titulo

class Escrito(models.Model):
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.autor.nome} - {self.livro.titulo}"

class Emprestimo(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="emprestimos")
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name="emprestimos")
    data_emprestimo = models.DateField(auto_now_add=True)
    data_devolucao = models.DateField(blank=True, null=True)

    
    def clean(self):
        # Verifica se o livro já está emprestado e não foi devolvido
        emprestimo_existente = Emprestimo.objects.filter(
            livro=self.livro,
            data_devolucao__isnull=True
        ).exclude(pk=self.pk).exists()

        if emprestimo_existente:
            raise ValidationError('Livro já está emprestado.')

        if self.data_devolucao and self.data_devolucao < self.data_emprestimo:
            raise ValidationError('Data de devolução deve ser posterior à data de empréstimo.')

        super().clean()

    
    def save(self, *args, **kwargs):
        self.full_clean()
        self.livro.situacao = "Emprestado"
        self.livro.save()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.aluno.nome} - {self.livro.titulo}"
    




# Comandos SQL.

# Inserir dados


# Inserir um aluno:
# INSERT INTO biblioteca_aluno (nome, cpf, email, telefone) VALUES ('João Silva', '12345678901', 'joao.silva@email.com', '11987654321');

# Inserir um autor:
# INSERT INTO biblioteca_autor (nome) VALUES ('Machado de Assis');

# Inserir um livro:
# INSERT INTO biblioteca_livro (isbn, titulo, situacao) VALUES ('9781234567897', 'Dom Casmurro', 'Disponível');

# Relacionar autor e livro (tabela Escrito):
# INSERT INTO biblioteca_escrito (autor_id, livro_id) VALUES (1, 1);

# Criar um empréstimo:
# INSERT INTO biblioteca_emprestimo (aluno_id, livro_id, data_emprestimo) VALUES (1, 1, '2025-01-04');


# Consultar dados


# Listar todos os alunos:
# SELECT * FROM biblioteca_aluno;

# Verificar quais livros estão disponíveis:
# SELECT * FROM biblioteca_livro WHERE situacao = 'Disponível';


# Atualizar dados


# Atualizar situação de um livro após empréstimo:
# UPDATE biblioteca_livro SET situacao = 'Emprestado' WHERE id = 1;

# Registrar devolução de um livro:
# UPDATE biblioteca_emprestimo SET data_devolucao = '2025-01-10' WHERE id = 1; 

# Alterar dados de um aluno:
# UPDATE biblioteca_aluno SET telefone = '11912345678' WHERE id = 1;


# Remover dados


# Excluir um aluno (e seus empréstimos associados):
# DELETE FROM biblioteca_emprestimo WHERE aluno_id = 1;
# DELETE FROM biblioteca_aluno WHERE id = 1;

# Remover um autor específico:
# DELETE FROM biblioteca_autor WHERE id = 1;

# Remover um livro e suas associações:
# DELETE FROM biblioteca_escrito WHERE livro_id = 1;
# DELETE FROM biblioteca_livro WHERE id = 1;
