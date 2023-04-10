;(function(){
    const modal = new bootstrap.Modal(document.getElementById('exampleModal'))
    const secondModal = new bootstrap.Modal(document.getElementById('afterModal'))

    htmx.on('htmx:afterSwap', (e) => {
        if (e.detail.target.id === "modal-dialog")
            modal.show()
    })
    htmx.on('htmx:beforeSwap', (e) => {
        if (e.detail.target.id === "modal-dialog" && !e.detail.xhr.response)
            modal.hide();
        if (e.detail.target.id === "modal-dialog" && !e.detail.xhr.response)
            secondModal.show();
    })
})()
