;(function(){
    const modal = new bootstrap.Modal(document.getElementById('exampleModal'))

    htmx.on('htmx:afterSwap', (e) => {
        if (e.detail.target.id === "modal-dialog")
            modal.show()
    })
    htmx.on('htmx:beforeSwap', (e) => {
        if (e.detail.target.id === "modal-dialog" && !e.detail.xhr.response)
            modal.hide()
    })
})()
