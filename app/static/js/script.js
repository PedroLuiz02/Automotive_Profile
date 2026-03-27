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

    let marcaSelecionada = document.querySelector(".marca_ativa");
    if (marcaSelecionada) {
    marcaAtual = marcaSelecionada.dataset.id;
    }
    
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
            tabelaAtual = 0;
            mostrarTabela();
            atualizarUI();
        };

        xhttp.open("GET", "/api/modelo/" + id + "/" + tipo);

        xhttp.send();
    };

    // Controle de Tabelas - Fichas
    let tabelaAtual = 0;
    const tabelas = ["tabela1", "tabela2"];

    function mostrarTabela() {
        tabelas.forEach(id => {
            const el = document.getElementById(id);
            if (el) el.style.display = "none";
        });
    
        const atual = document.getElementById(tabelas[tabelaAtual]);
        if (atual) atual.style.display = "block";
    }
    
    window.mudarTabela = function(direcao) {
        tabelaAtual += direcao;
    
        if (tabelaAtual < 0) tabelaAtual = 0;
        if (tabelaAtual >= tabelas.length) tabelaAtual = tabelas.length - 1;
    
        tabelas.forEach(id => {
            document.getElementById(id).style.display = "none";
        });
    
        document.getElementById(tabelas[tabelaAtual]).style.display = "block";
    
        atualizarUI();
    }
    
    function atualizarUI() {
        document.getElementById("pagina").innerText = `${tabelaAtual + 1} / ${tabelas.length}`;
    
        document.getElementById("seta-esq").style.display = tabelaAtual === 0 ? "none" : "block";
        document.getElementById("seta-dir").style.display = tabelaAtual === tabelas.length - 1 ? "none" : "block";
    }

});
