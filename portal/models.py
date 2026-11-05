from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

# Slug do conteúdo que funciona como página inicial do portal (URL "/").
SLUG_INICIO = "inicio"


class Conteudo(models.Model):
    """Página do portal. O HTML interno de cada página fica guardado no banco de dados."""

    titulo = models.CharField("título", max_length=100)
    slug = models.SlugField(
        "slug",
        max_length=100,
        unique=True,
        help_text="Parte da URL do conteúdo. Ex.: meu-tema vira /conteudo/meu-tema/",
    )
    conteudo_html = models.TextField(
        "conteúdo HTML",
        help_text="Somente o HTML interno da página (section, article, h2, p...). "
                  "Não coloque html, head, body, header, nav nem footer aqui.",
    )
    ativo = models.BooleanField("ativo", default=True)

    class Meta:
        verbose_name = "conteúdo"
        verbose_name_plural = "conteúdos"
        ordering = ["titulo"]

    def __str__(self):
        return self.titulo

    def get_url(self):
        # O conteúdo inicial usa a URL "/"; os demais usam /conteudo/<slug>/.
        if self.slug == SLUG_INICIO:
            return reverse("inicio")
        return reverse("conteudo", args=[self.slug])


class Menu(models.Model):
    """Item da navegação do portal. Pode levar a um Conteudo interno ou a um link externo."""

    TIPO_INTERNO = "interno"
    TIPO_EXTERNO = "externo"
    TIPOS_DESTINO = [
        (TIPO_INTERNO, "Conteúdo interno"),
        (TIPO_EXTERNO, "Link externo"),
    ]

    titulo = models.CharField("título", max_length=50)
    tipo_destino = models.CharField(
        "tipo de destino",
        max_length=10,
        choices=TIPOS_DESTINO,
        default=TIPO_INTERNO,
    )
    ordem = models.PositiveIntegerField(
        "ordem",
        default=0,
        help_text="Itens com número menor aparecem primeiro no menu.",
    )
    ativo = models.BooleanField("ativo", default=True)

    # Só é usado quando o tipo de destino é "Conteúdo interno".
    conteudo = models.ForeignKey(
        Conteudo,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="itens_menu",
        verbose_name="conteúdo",
        help_text="Preencha quando o destino for um conteúdo interno.",
    )

    # Só é usado quando o tipo de destino é "Link externo".
    url_externa = models.URLField(
        "URL externa",
        blank=True,
        help_text="Preencha quando o destino for um link externo. Ex.: https://www.w3schools.com",
    )

    class Meta:
        verbose_name = "item do menu"
        verbose_name_plural = "itens do menu"
        ordering = ["ordem", "titulo"]

    def __str__(self):
        return self.titulo

    def clean(self):
        # Valida o formulário do Admin: cada tipo de destino exige o seu campo.
        if self.tipo_destino == self.TIPO_INTERNO:
            if not self.conteudo:
                raise ValidationError({"conteudo": "Escolha um conteúdo para o item de destino interno."})
            self.url_externa = ""
        elif self.tipo_destino == self.TIPO_EXTERNO:
            if not self.url_externa:
                raise ValidationError({"url_externa": "Informe a URL para o item de link externo."})
            self.conteudo = None

    def get_url(self):
        if self.tipo_destino == self.TIPO_EXTERNO:
            return self.url_externa
        return self.conteudo.get_url()
