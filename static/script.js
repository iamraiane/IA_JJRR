async function traduzirTexto() {
    const texto = document.getElementById("texto").value;
    const idioma = document.getElementById("idioma").value;

    const resultado = document.getElementById("traducao");
    const mensagem = document.getElementById("mensagem");

    const botao = document.getElementById("botao");

    mensagem.textContent = "";

    if (!texto.trim()) {
        mensagem.textContent = "Digite um texto antes de traduzir.";
        return;
    }

    resultado.textContent = "Traduzindo...";
    resultado.classList.remove("pronto");
    botao.disabled = true;

    try {
        const resposta = await fetch("/traduzir", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                texto: texto,
                idioma_destino: idioma
            })
        });

        const dados = await resposta.json();

        if (!resposta.ok) {
            throw new Error(dados.erro || "Erro ao traduzir.");
        }

        resultado.textContent = dados.traducao;
        resultado.classList.add("pronto");

    } catch (erro) {
        resultado.textContent = "Não foi possível realizar a tradução.";
        mensagem.textContent = erro.message;
    } finally {
        botao.disabled = false;
    }
}

// Ctrl + Enter traduz
document.getElementById("texto").addEventListener("keydown", function (e) {
    if (e.ctrlKey && e.key === "Enter") traduzirTexto();
});
