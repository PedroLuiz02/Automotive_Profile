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

    let marcaAtual = null;
    
    // Ajax de Troca de Marcas
    function trocar_marca(id){
        const xhttp = new XMLHttpRequest();
        xhttp.onload = function(){
            document.getElementById('lista_carros').innerHTML = this.responseText;
            ativarOpenModal();
            ativarCloseModal();
        };

        if (marcaAtual == null) {
        xhttp.open("GET", "/api/carros");
        } else {
        xhttp.open("GET", "/api/carros/" + id);
        }

        xhttp.send();
    };

    // Evento de Troca de Marca
    document.querySelectorAll(".marca").forEach(el => {
        el.addEventListener("click", function() {
            
            let id = this.dataset.id;

            if (marcaAtual == id) {
                document.querySelectorAll(".marca").forEach(b => {
                    b.classList.remove("marca_ativa");
                });
    
                marcaAtual = null;
    
            } else {
                document.querySelectorAll(".marca").forEach(b => {
                    b.classList.remove("marca_ativa");
                });
    
                this.classList.add("marca_ativa");
    
                marcaAtual = id;
            }

            trocar_marca(id)
        })
    });

    // Evento no botão de abas
    document.querySelectorAll(".swap-btn").forEach(btn => {
        btn.addEventListener("click", function() {
            let tipo = this.dataset.tipo;
            let id = this.dataset.id;
            console.log(tipo);
            console.log(id);

            document.querySelectorAll(".swap-btn").forEach(b => {
                b.classList.remove("ativo");
            });
    
            this.classList.add("ativo");
    
            trocar_aba(id, tipo);
        });
    });

    let geralBtn = document.querySelector(".swap-btn.ativo");

    let tipo = geralBtn.dataset.tipo;
    let id = geralBtn.dataset.id;

    trocar_aba(id, tipo);
    
    // Ajax de Troca de Abas
    function trocar_aba(id, tipo){
        const xhttp = new XMLHttpRequest();
        xhttp.onload = function(){
            document.getElementById('model-content').innerHTML = this.responseText;
            ativarOpenModal();
            ativarCloseModal();
        };

        xhttp.open("GET", "/api/modelo/" + id + "/" + tipo);

        xhttp.send();
    };
});