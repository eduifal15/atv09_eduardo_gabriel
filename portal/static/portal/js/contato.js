// GABRIEL BARBOSA DA SILVA E EDUARDO JOAQUIM SANTOS DA SILVA - ATV09 - Turma 513
// JavaScript do formulário de Contato / Ouvidoria (veio da ATV07).
// A navegação do portal NÃO usa JavaScript: ela é feita pelas URLs e Views do Django.

// Função chamada no evento onsubmit do formulário de Contato/Ouvidoria.
// Ela intercepta o envio para mostrar um resumo de revisão antes de mandar os dados de verdade.
function confirmarEnvio(evento) {

    var form = evento.target;

    // Primeiro, deixamos o próprio navegador validar os campos (required, pattern, minlength...).
    // Isso ativa também os estados visuais :valid / :invalid do CSS.
    if (!form.checkValidity()) {
        form.reportValidity();
        return false; // impede o envio até os campos ficarem válidos
    }

    // Captura os valores digitados para montar o resumo de revisão.
    var nome = form.nome.value;
    var email = form.email.value;
    var telefone = form.telefone.value;
    var assunto = form.assunto.options[form.assunto.selectedIndex].text;
    var mensagem = form.mensagem.value;

    // Descobre qual radio de perfil foi marcado.
    var perfil = "";
    var radiosPerfil = form.querySelectorAll('input[name="perfil"]');
    radiosPerfil.forEach(function (radio) {
        if (radio.checked) {
            perfil = radio.value;
        }
    });

    // Monta o texto do resumo de revisão.
    var resumo =
        "Revise os dados antes de enviar:\n\n" +
        "Nome: " + nome + "\n" +
        "E-mail: " + email + "\n" +
        "Telefone: " + telefone + "\n" +
        "Assunto: " + assunto + "\n" +
        "Perfil: " + perfil + "\n" +
        "Mensagem: " + mensagem + "\n\n" +
        "Clique em OK para confirmar o envio ou em Cancelar para corrigir os dados.";

    // confirm() retorna true (OK) ou false (Cancelar).
    var confirmou = confirm(resumo);

    // Se cancelou, retornamos false: o envio é impedido e os dados continuam preenchidos no formulário.
    // Se confirmou, retornamos true: o formulário segue com o envio real via GET.
    return confirmou;
}
