from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Conteudo, Menu


class PortalTests(TestCase):
    def setUp(self):
        self.inicio = Conteudo.objects.create(
            titulo="Início", slug="inicio", conteudo_html="<section><h2>Página inicial</h2></section>"
        )
        self.tema = Conteudo.objects.create(
            titulo="Meu Tema", slug="meu-tema", conteudo_html="<section><h2>Texto do tema</h2></section>"
        )
        Menu.objects.create(titulo="Meu Tema", tipo_destino="interno", ordem=2, conteudo=self.tema)
        Menu.objects.create(titulo="Início", tipo_destino="interno", ordem=1, conteudo=self.inicio)
        Menu.objects.create(
            titulo="W3Schools", tipo_destino="externo", ordem=3, url_externa="https://www.w3schools.com"
        )

    def test_pagina_inicial(self):
        resposta = self.client.get("/")
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "<h2>Página inicial</h2>", html=True)

    def test_conteudo_pelo_slug_vem_do_banco(self):
        resposta = self.client.get("/conteudo/meu-tema/")
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Texto do tema")

    def test_conteudo_inativo_ou_inexistente_da_404(self):
        self.tema.ativo = False
        self.tema.save()
        self.assertEqual(self.client.get("/conteudo/meu-tema/").status_code, 404)
        self.assertEqual(self.client.get("/conteudo/nao-existe/").status_code, 404)

    def test_menu_dinamico_na_ordem_certa(self):
        resposta = self.client.get("/")
        self.assertEqual([item.titulo for item in resposta.context["menu"]], ["Início", "Meu Tema", "W3Schools"])
        self.assertContains(resposta, 'href="/conteudo/meu-tema/"')
        self.assertContains(resposta, 'href="https://www.w3schools.com"')

    def test_item_de_menu_inativo_nao_aparece(self):
        Menu.objects.filter(titulo="W3Schools").update(ativo=False)
        resposta = self.client.get("/")
        self.assertNotContains(resposta, "W3Schools")

    def test_item_interno_some_se_o_conteudo_estiver_inativo(self):
        self.tema.ativo = False
        self.tema.save()
        resposta = self.client.get("/")
        self.assertNotContains(resposta, "/conteudo/meu-tema/")

    def test_menu_interno_precisa_de_conteudo_e_externo_precisa_de_url(self):
        with self.assertRaises(ValidationError):
            Menu(titulo="Sem destino", tipo_destino="interno").full_clean()
        with self.assertRaises(ValidationError):
            Menu(titulo="Sem url", tipo_destino="externo").full_clean()

    def test_mensagem_enviada(self):
        url = reverse("mensagem_enviada") + "?nome=Ana&email=ana@exemplo.com&mensagem=Ola"
        resposta = self.client.get(url)
        self.assertContains(resposta, "Obrigado, Ana!")
        resposta = self.client.get(reverse("mensagem_enviada"))
        self.assertContains(resposta, "Nenhum dado de formulário")
