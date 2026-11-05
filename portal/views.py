from django.shortcuts import get_object_or_404, render

from .models import SLUG_INICIO, Conteudo, Menu


def obter_itens_menu():
    """Busca no banco os itens ativos do menu, já na ordem definida no Django Admin."""
    # Item interno só aparece se o conteúdo dele também estiver ativo.
    itens = Menu.objects.filter(ativo=True).select_related("conteudo").order_by("ordem", "titulo")
    return [
        item for item in itens
        if item.tipo_destino == Menu.TIPO_EXTERNO or (item.conteudo and item.conteudo.ativo)
    ]


def pagina_inicial(request):
    """Página inicial (URL "/"): mostra o conteúdo cujo slug é 'inicio'."""
    conteudo = get_object_or_404(Conteudo, slug=SLUG_INICIO, ativo=True)
    contexto = {
        "conteudo": conteudo,
        "menu": obter_itens_menu(),
    }
    return render(request, "portal/conteudo.html", contexto)


def exibir_conteudo(request, slug):
    """Mostra um conteúdo qualquer, escolhido pelo slug que vem na URL."""
    conteudo = get_object_or_404(Conteudo, slug=slug, ativo=True)
    contexto = {
        "conteudo": conteudo,
        "menu": obter_itens_menu(),
    }
    return render(request, "portal/conteudo.html", contexto)


def mensagem_enviada(request):
    """Página de destino do formulário de Contato (que usa o método GET)."""
    nome = request.GET.get("nome")
    email = request.GET.get("email")

    # Campos que o formulário envia, na ordem em que aparecem na tabela-resumo.
    campos = [
        ("Nome", nome),
        ("E-mail", email),
        ("Telefone", request.GET.get("telefone")),
        ("Assunto", request.GET.get("assunto")),
        ("Perfil", request.GET.get("perfil")),
        ("Mensagem", request.GET.get("mensagem")),
    ]

    contexto = {
        "menu": obter_itens_menu(),
        # Só mostra o resumo se os dados realmente vieram do formulário.
        "recebeu_dados": bool(nome and email),
        "nome": nome,
        "email": email,
        "campos": [(rotulo, valor or "-") for rotulo, valor in campos],
    }
    return render(request, "portal/mensagem_enviada.html", contexto)
