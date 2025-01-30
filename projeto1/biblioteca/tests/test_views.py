from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from biblioteca.models import Aluno, Autor, Livro, Emprestimo


class LoginRequiredMixinTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_login_required_views(self):
        protected_urls = [
            reverse("aluno_list"),
            reverse("autor_list"),
            reverse("livro_list"),
            reverse("emprestimo_list"),
        ]
        for url in protected_urls:
            response = self.client.get(url)
            self.assertRedirects(response, f"/login/?next={url}")


class AlunoViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        self.aluno = Aluno.objects.create(nome="Teste Aluno", cpf="12345678901", email="teste@exemplo.com", telefone="123456789")

    def test_aluno_list_view(self):
        response = self.client.get(reverse("aluno_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Teste Aluno")

    def test_aluno_create_view(self):
        response = self.client.post(reverse("aluno_create"), {
            "nome": "Novo Aluno",
            "cpf": "09876543210",
            "email": "novo@exemplo.com",
            "telefone": "987654321",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Aluno.objects.filter(nome="Novo Aluno").exists())

    def test_aluno_update_view(self):
        response = self.client.post(reverse("aluno_update", args=[self.aluno.pk]), {
            "nome": "Aluno Atualizado",
            "cpf": "12345678901",
            "email": "atualizado@exemplo.com",
            "telefone": "123456789",
        })
        self.assertEqual(response.status_code, 302)
        self.aluno.refresh_from_db()
        self.assertEqual(self.aluno.nome, "Aluno Atualizado")

    def test_aluno_delete_view(self):
        response = self.client.post(reverse("aluno_delete", args=[self.aluno.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Aluno.objects.filter(pk=self.aluno.pk).exists())


class AutorViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        self.autor = Autor.objects.create(nome="Autor Teste")

    def test_autor_list_view(self):
        response = self.client.get(reverse("autor_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Autor Teste")

    def test_autor_create_view(self):
        response = self.client.post(reverse("autor_create"), {"nome": "Novo Autor"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Autor.objects.filter(nome="Novo Autor").exists())

    def test_autor_update_view(self):
        response = self.client.post(reverse("autor_update", args=[self.autor.pk]), {"nome": "Autor Atualizado"})
        self.assertEqual(response.status_code, 302)
        self.autor.refresh_from_db()
        self.assertEqual(self.autor.nome, "Autor Atualizado")

    def test_autor_delete_view(self):
        response = self.client.post(reverse("autor_delete", args=[self.autor.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Autor.objects.filter(pk=self.autor.pk).exists())


class LivroViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="usuario", password="senha")
        self.client.login(username="usuario", password="senha")
        self.autor = Autor.objects.create(nome="Autor Teste") 
        self.livro = Livro.objects.create(isbn="123456789", titulo="Livro Teste", situacao="Disponível")

    def test_livro_list_view(self):
        response = self.client.get(reverse("livro_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Livro Teste")

    def test_livro_create_view(self):
        response = self.client.post(reverse("livro_create"), {
            "isbn": "987654321",
            "titulo": "Novo Livro",
            "situacao": "Disponível",
            "autores": [self.autor.pk],
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('livro_list')) 
        self.assertTrue(Livro.objects.filter(titulo="Novo Livro").exists())

    def test_livro_update_view(self):
        response = self.client.post(reverse("livro_update", args=[self.livro.pk]), {
            "isbn": "123456789",
            "titulo": "Livro Atualizado",
            "situacao": "Disponível",
            "autores": [self.autor.pk],
        })
        self.assertEqual(response.status_code, 302)
        self.livro.refresh_from_db()
        self.assertEqual(self.livro.titulo, "Livro Atualizado")

    def test_livro_delete_view(self):
        response = self.client.post(reverse("livro_delete", args=[self.livro.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Livro.objects.filter(pk=self.livro.pk).exists())


class EmprestimoViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        self.aluno = Aluno.objects.create(nome="Teste Aluno", cpf="12345678901", email="teste@exemplo.com", telefone="123456789")
        self.livro = Livro.objects.create(isbn="123456789", titulo="Livro Teste", situacao="Disponível")
        self.emprestimo = Emprestimo.objects.create(aluno=self.aluno, livro=self.livro, data_devolucao="2025-12-31")

    def test_emprestimo_list_view(self):
        response = self.client.get(reverse("emprestimo_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Livro Teste")

    def test_emprestimo_create_view(self):
        response = self.client.post(reverse("emprestimo_create"), {
            "aluno": self.aluno.pk,
            "livro": self.livro.pk,
            "data_devolucao": "2026-01-01",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Emprestimo.objects.filter(data_devolucao="2026-01-01").exists())

    def test_emprestimo_update_view(self):
        response = self.client.post(reverse("emprestimo_update", args=[self.emprestimo.pk]), {
            "aluno": self.aluno.pk,
            "livro": self.livro.pk,
            "data_devolucao": "2026-12-31",
        })
        self.assertEqual(response.status_code, 302)
        self.emprestimo.refresh_from_db()
        self.assertEqual(str(self.emprestimo.data_devolucao), "2026-12-31")

    def test_emprestimo_delete_view(self):
        response = self.client.post(reverse("emprestimo_delete", args=[self.emprestimo.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Emprestimo.objects.filter(pk=self.emprestimo.pk).exists())
