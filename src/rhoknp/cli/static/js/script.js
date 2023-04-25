/* Keep the status of the accordion to show analysis results */
const defaultOpenAccordionItems = document.querySelectorAll(
  ".accordion-item-default-open"
);
defaultOpenAccordionItems.forEach((item) => {
  const itemId = `accordion-${item.id}`;
  if (localStorage.getItem(itemId) === null) {
    localStorage.setItem(itemId, "true");
  }
});

const accordionItems = document.querySelectorAll(".accordion-item");
accordionItems.forEach((item) => {
  const itemId = `accordion-${item.id}`;
  item.addEventListener("shown.bs.collapse", () => {
    localStorage.setItem(itemId, "true");
  });
  item.addEventListener("hidden.bs.collapse", () => {
    localStorage.setItem(itemId, "false");
  });
});

accordionItems.forEach((item) => {
  const itemId = `accordion-${item.id}`;
  const state = localStorage.getItem(itemId);
  console.log(state);
  if (state === "true") {
    item.querySelector(".accordion-button").classList.remove("collapsed");
    item.querySelector(".accordion-collapse").classList.add("show");
  } else {
    item.querySelector(".accordion-button").classList.add("collapsed");
    item.querySelector(".accordion-collapse").classList.remove("show");
  }
});

const showAllButton = document.querySelector("#show-all-button");
showAllButton.addEventListener("click", () => {
  accordionItems.forEach((item) => {
    const itemId = `accordion-${item.id}`;
    localStorage.setItem(itemId, "true");
    item.querySelector(".accordion-button").classList.remove("collapsed");
    item.querySelector(".accordion-collapse").classList.add("show");
  });
});

const hideAllButton = document.querySelector("#hide-all-button");
hideAllButton.addEventListener("click", () => {
  accordionItems.forEach((item) => {
    const itemId = `accordion-${item.id}`;
    localStorage.setItem(itemId, "false");
    item.querySelector(".accordion-button").classList.add("collapsed");
    item.querySelector(".accordion-collapse").classList.remove("show");
  });
});
