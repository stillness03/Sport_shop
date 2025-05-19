document.addEventListener("DOMContentLoaded", function () {
  const input = document.getElementById("gym-search");
  const button = document.getElementById("search-button");

  function performSearch() {
    const searchTerm = input.value.toLowerCase();
    const gymCards = document.querySelectorAll(".gym-card");
    const cityHeaders = document.querySelectorAll(".city-header");

    let firstMatchCoords = null;
    let foundGymId = null;

    const gymsData = JSON.parse(
      document.getElementById("gyms-data").textContent
    );
    const match = gymsData.find((gym) => {
      const name = gym.name.toLowerCase();
      const address = gym.address.toLowerCase();
      const city = gym.address.split(",").slice(-2, -1)[0].toLowerCase();
      return (
        name.includes(searchTerm) ||
        address.includes(searchTerm) ||
        city.includes(searchTerm)
      );
    });

    if (match) {
      firstMatchCoords = [match.latitude, match.longitude];
      foundGymId = match.id;
    }

    gymCards.forEach((card) => {
      const gymName = card
        .querySelector(".card-title")
        .textContent.toLowerCase();
      const gymAddress = card
        .querySelector(".card-text")
        .textContent.toLowerCase();
      const cityName = card.dataset.city?.toLowerCase() || "";

      const isMatch =
        gymName.includes(searchTerm) ||
        gymAddress.includes(searchTerm) ||
        cityName.includes(searchTerm);
      card.style.display = isMatch ? "block" : "none";
    });

    cityHeaders.forEach((header) => {
      const cityCards = header.nextElementSibling.querySelectorAll(".gym-card");
      const hasVisible = Array.from(cityCards).some(
        (card) => card.style.display !== "none"
      );
      header.style.display = hasVisible ? "block" : "none";
      header.nextElementSibling.style.display = hasVisible ? "block" : "none";
    });

    if (firstMatchCoords && typeof map !== "undefined") {
      map.setView(firstMatchCoords, 14);
      updateVisibleGyms(gymsData);
    }
  }

  input.addEventListener("input", performSearch);
  button.addEventListener("click", performSearch);

  input.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      e.preventDefault();
      performSearch();
    }
  });

  document
    .getElementById("back-to-list")
    .addEventListener("click", function () {
      document.getElementById("gym-list").style.display = "block";
      document.getElementById("gym-detail").style.display = "none";
    });
});
