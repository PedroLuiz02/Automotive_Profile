document.addEventListener('DOMContentLoaded', function() {
    // timestamp
    function atualizarTempo() {
        const agora = new Date()

        const formato = agora.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: true
        })
        document.getElementById("timestamp").textContent = formato
    }

    setInterval(atualizarTempo, 1000)
    atualizarTempo()
})