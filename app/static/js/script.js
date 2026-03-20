document.addEventListener('DOMContentLoaded', function() {

    function ativarOpenModal(){
        console.log("ativando modal");

        const openButtons = document.querySelectorAll(".open-modal");

        openButtons.forEach(button => {
            button.addEventListener("click", () => {
                console.log("clicou");

                const modalId = button.getAttribute("data-modal");
                const modal = document.getElementById(modalId);
                console.log("modalId:", modalId);
                console.log("modal:", modal);
                modal.showModal();
            });
        });
    };
    
    function ativarCloseModal(){
        const closeButtons = document.querySelectorAll(".close-modal");

        closeButtons.forEach(button => {
            button.addEventListener("click", () => {
                const modalId = button.getAttribute("data-modal");
                const modal = document.getElementById(modalId);
                modal.close();
            });
        });
    };

    ativarOpenModal();
    ativarCloseModal();

    document.querySelectorAll(".marca").forEach(el => {
        el.addEventListener("click", function() {
            trocar_marca(this.dataset.id)
        })
    });

    let marcaAtual = null;
    
    function trocar_marca(id){
        const xhttp = new XMLHttpRequest();
        xhttp.onload = function(){
            document.getElementById('lista_carros').innerHTML = this.responseText;
            ativarOpenModal()
            ativarCloseModal()
        }

        if (marcaAtual == id) {
        xhttp.open("GET", "/api/carros");
        marcaAtual = null;

        } else {
        xhttp.open("GET", "/api/carros/" + id);
        marcaAtual = id;
        }

        xhttp.send();
    };
})