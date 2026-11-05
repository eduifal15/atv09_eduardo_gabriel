from django.urls import path

from . import views

urlpatterns = [
    # Página inicial.
    path("", views.pagina_inicial, name="inicio"),
    # URL dinâmica: o slug do conteúdo vem na própria URL.
    path("conteudo/<slug:slug>/", views.exibir_conteudo, name="conteudo"),
    # Página mostrada depois do envio do formulário de Contato.
    path("mensagem-enviada/", views.mensagem_enviada, name="mensagem_enviada"),
]
