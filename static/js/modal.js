;(function(){
    const modal = new bootstrap.Modal(document.getElementById('exampleModal'))
    const secondModal = new bootstrap.Modal(document.getElementById('afterModal'))
    const thirdModal = new bootstrap.Modal(document.getElementById('email-modal'))
    const fourthModal = new bootstrap.Modal(document.getElementById('cart-modal'))
    const fifthModal = new bootstrap.Modal(document.getElementById('quick-view-modal'))

    htmx.on('htmx:afterSwap', (e) => {
        if (e.detail.target.id === "modal-dialog")
            modal.show()
    })
    htmx.on('htmx:beforeSwap', (e) => {
        if (e.detail.target.id === "modal-dialog" && !e.detail.xhr.response)
            modal.hide();

        if (e.detail.target.id === "emailModal" && !e.detail.xhr.response)
            thirdModal.show();

        if (e.detail.target.id === "modal-dialog" && !e.detail.xhr.response)
            secondModal.show();

    })
    htmx.on('htmx:afterSwap', (e) => {
        if (e.detail.target.id === "carIcon")
            location.reload();
    })

    htmx.on('htmx:afterSwap', (e) => {
        if (e.detail.target.id === "productForCart")
            fourthModal.show();
    })

    htmx.on('htmx:afterSwap', (e) => {
        if (e.detail.target.id === "quickViewModal")
            fifthModal.show();
    })

})()

const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))
