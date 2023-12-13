function removeAcao(acaoId) {
    fetch("/remove-Acao", {
        method: 'POST',
        body: JSON.stringify({acaoId: acaoId}),
    }).then(() => {
        window.location.href="/acoes"
    });
}
function atualizaAcao(acaoId) {
    fetch("/atualiza-Acao", {
        method: 'POST',
        body: JSON.stringify({acaoId: acaoId}),
    }).then(() => {
        window.location.href = "/acoes"
    })
}
function removeCrypto(cryptoId) {
    fetch("/remove-Crypto", {
        method: 'POST',
        body: JSON.stringify({cryptoId: cryptoId}),
    }).then(() => {
        window.location.href="/cryptos"
    });
}
function atualizaCrypto(cryptoId) {
    fetch("/atualiza-Crypto", {
        method: 'POST',
        body: JSON.stringify({cryptoId: cryptoId}),
    }).then(() => {
        window.location.href = "/cryptos"
    })
}