document.addEventListener("DOMContentLoaded", function() {

    const botao = document.getElementById("btnNovaMovimentacao");
    const modal = document.getElementById("modalMovimentacao");
    const fechar = document.getElementById("fecharModal");
    const cancelar = document.getElementById("cancelarMovimentacao");

    botao.addEventListener("click", function() {
        modal.classList.add("mostrar");
    });

    fechar.addEventListener("click", function() {
        modal.classList.remove("mostrar");
    });

    cancelar.addEventListener("click", function() {
        modal.classList.remove("mostrar");
    });

});