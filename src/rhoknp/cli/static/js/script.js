/* Keep the status of the accordion to show analysis results */
const accordionItems = document.querySelectorAll(".accordion-item");

accordionItems.forEach((item) => {
    item.addEventListener("shown.bs.collapse", () => {
        localStorage.setItem("accordion-" + item.id, "true")
    })
})

accordionItems.forEach((item) => {
    item.addEventListener("hidden.bs.collapse", () => {
        localStorage.removeItem("accordion-" + item.id)
    })
})

accordionItems.forEach((item) => {
    const state = localStorage.getItem("accordion-" + item.id)
    if (state === "true") {
        item.querySelector(".accordion-button").classList.remove("collapsed")
        item.querySelector(".accordion-collapse").classList.add("show")
    }
})
