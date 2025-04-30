document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("gym-search").addEventListener("input", function (e) {
    const searchTerm = e.target.value.toLowerCase();
    const gymCards = document.querySelectorAll(".gym-card");
    const cityHeaders = document.querySelectorAll(".city-header");

    let hasVisibleCards = false;

    gymCards.forEach((card) => {
      const gymName = card
        .querySelector(".card-title")
        .textContent.toLowerCase();
      const gymAddress = card
        .querySelector(".card-text")
        .textContent.toLowerCase();

      if (gymName.includes(searchTerm) || gymAddress.includes(searchTerm)) {
        card.style.display = "block";
        hasVisibleCards = true;
      } else {
        card.style.display = "none";
      }
    });

    cityHeaders.forEach((header) => {
      const cityCards = header.nextElementSibling.querySelectorAll(".gym-card");
      const hasVisible = Array.from(cityCards).some(
        (card) => card.style.display !== "none"
      );

      if (hasVisible) {
        header.style.display = "block";
        header.nextElementSibling.style.display = "block";
      } else {
        header.style.display = "none";
        header.nextElementSibling.style.display = "none";
      }
    });
  });

  document
    .getElementById("back-to-list")
    .addEventListener("click", function () {
      document.getElementById("gym-list").style.display = "block";
      document.getElementById("gym-detail").style.display = "none";
    });
});
