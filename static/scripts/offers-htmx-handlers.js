// replace <span id="offers-in-cart-counter"> inner value with reduced one on offer removed from cart
document.addEventListener('htmx:afterOnLoad', function(event) {
    if (event?.detail?.requestConfig?.elt?.id !== "remove-offer-button") {
        return
    }
    const counter = document.querySelector("#offers-in-cart-counter")
    const currentCount = parseInt(counter.textContent, 10);

    if (!isNaN(currentCount) && currentCount > 0) {
        counter.textContent = String(currentCount - 1);
    }
});

// htmx handlers
function htmxHandlers() {
    console.log("i am called")
    htmx.on("showMessage", (e) => {
      const toastElement = document.getElementById("toast")
      const toastBody = document.getElementById("toast-body")
      const toast = new bootstrap.Toast(toastElement, { delay: 2000 })
      toastBody.innerText = e.detail.value
      toast.show()
    })

    htmx.on("showError", (e) => {
      const toastElement = document.getElementById("toast-warning")
      const toastBody = document.getElementById("toast-warning-body")
      const toast = new bootstrap.Toast(toastElement, { delay: 2000 })
      toastBody.innerText = e.detail.value
      toast.show()
    })

    const modal = new bootstrap.Modal(document.getElementById("modal"))

    htmx.on("htmx:afterSwap", (e) => {
      // Response targeting #dialog => show the modal
      if (e.detail.target.id == "dialog") {
        modal.show()
      }
    })

    htmx.on("htmx:beforeSwap", (e) => {
    // Empty response targeting #cart_modal_form => hide the modal
    if (e.detail.target.id == "cart_modal_form" && !e.detail.xhr.response) {
      modal.hide()
      e.detail.shouldSwap = false
      const counter = document.querySelector("#offers-in-cart-counter")
      counter.textContent = String(0);
    }
    })

    // Remove dialog content after hiding
    htmx.on("hidden.bs.modal", () => {
      document.getElementById("dialog").innerHTML = ""
    })
}

document.addEventListener('DOMContentLoaded', function() {
    htmxHandlers()
});
