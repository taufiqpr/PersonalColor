document.addEventListener("DOMContentLoaded", function () {
  const filterCheckboxes = document.querySelectorAll(".form-check-input");
  const clearAllButton = document.querySelector(".clear-all");
  const productCards = document.querySelectorAll(".product-card");

  function applyFilters() {
    const activeFilters = {
      color: [],
      status: [],
    };

    filterCheckboxes.forEach((checkbox) => {
      if (checkbox.checked) {
        if (checkbox.id.startsWith("type")) {
          activeFilters.color.push(checkbox.nextElementSibling.textContent.trim().toLowerCase());
        } else if (checkbox.id.startsWith("status")) {
          activeFilters.status.push(checkbox.nextElementSibling.textContent.trim().toLowerCase());
        }
      }
    });

    productCards.forEach((card) => {
      const cardColor = card.dataset.color;
      const cardStatus = card.dataset.status;

      const colorMatch = activeFilters.color.length === 0 || activeFilters.color.includes(cardColor);
      const statusMatch = activeFilters.status.length === 0 || activeFilters.status.includes(cardStatus);

      if (colorMatch && statusMatch) {
        card.closest(".col-md-4").style.display = "";
      } else {
        card.closest(".col-md-4").style.display = "none";
      }
    });
  }

  filterCheckboxes.forEach((checkbox) => {
    checkbox.addEventListener("change", applyFilters);
  });

  clearAllButton.addEventListener("click", function () {
    filterCheckboxes.forEach((checkbox) => {
      checkbox.checked = false;
    });
    productCards.forEach((card) => {
      card.closest(".col-md-4").style.display = "";
    });
  });
});
