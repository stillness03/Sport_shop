let map;
let markers = [];

document.addEventListener("DOMContentLoaded", function () {
  const gymsData = JSON.parse(document.getElementById("gyms-data").textContent);

  map = L.map("map", {
    center: [40.7128, -74.006],
    zoom: 12,
    zoomControl: false,
  });

  L.tileLayer(
    "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
    {
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }
  ).addTo(map);

  const customIcon = L.icon({
    iconUrl: "/static/img/marker.png",
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -32],
  });

  addMarkers(gymsData, customIcon);

  map.on("moveend", function () {
    updateVisibleGyms(gymsData);
  });

  updateVisibleGyms(gymsData);
});

function addMarkers(gyms, customIcon) {
  markers.forEach((marker) => map.removeLayer(marker));
  markers = [];

  gyms.forEach((gym) => {
    if (gym.latitude && gym.longitude) {
      const marker = L.marker([gym.latitude, gym.longitude], {
        icon: customIcon,
      })
        .addTo(map)
        .bindPopup(`<b>${gym.name}</b><br>${gym.address}`);
      marker.on("click", () => {
        window.loadGymDetail(gym.id);
      });

      markers.push(marker);
    }
  });
}

function updateVisibleGyms(gyms) {
  if (!map) return;

  const bounds = map.getBounds();
  const center = bounds.getCenter();

  const visibleGyms = gyms.filter((gym) => {
    if (!gym.latitude || !gym.longitude) return false;

    const gymLatLng = L.latLng(gym.latitude, gym.longitude);

    if (bounds.contains(gymLatLng)) return true;

    return center.distanceTo(gymLatLng) <= 50000;
  });

  const cities = {};
  visibleGyms.forEach((gym) => {
    const city = extractCityFromAddress(gym.address);
    if (!cities[city]) cities[city] = [];
    cities[city].push(gym);
  });

  const gymList = document.getElementById("gym-list");
  gymList.innerHTML = "";

  if (visibleGyms.length === 0) {
    gymList.innerHTML = '<p class="text-muted">No gyms found in this area</p>';
    return;
  }

  const sortedCities = Object.keys(cities).sort((a, b) => {
    const gymA = cities[a][0];
    const gymB = cities[b][0];
    const distA = L.latLng(center).distanceTo(
      L.latLng(gymA.latitude, gymA.longitude)
    );
    const distB = L.latLng(center).distanceTo(
      L.latLng(gymB.latitude, gymB.longitude)
    );
    return distA - distB;
  });

  sortedCities.forEach((city) => {
    const cityHeader = document.createElement("h5");
    cityHeader.className = "mt-4 mb-3 city-header";
    cityHeader.textContent = city;
    gymList.appendChild(cityHeader);

    cities[city].forEach((gym) => {
      const gymCard = document.createElement("div");
      gymCard.className = "gym-card mb-3";
      gymCard.setAttribute("data-gym-id", gym.id);
      gymCard.innerHTML = `
                <div class="card-body">
                    <h5 class="card-title">${gym.name}</h5>
                    <p class="card-text text-muted">${gym.address}</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <span class="badge bg-success">${Math.round(
                          center.distanceTo(
                            L.latLng(gym.latitude, gym.longitude)
                          ) / 1000
                        )} km away</span>
                        <button class="btn btn-sm btn-outline-primary view-gym-btn" data-gym-id="${
                          gym.id
                        }">VIEW DETAILS →</button>
                    </div>
                </div>
            `;
      gymList.appendChild(gymCard);
    });
  });

  initGymCardHandlers();
}

function initGymCardHandlers() {
  document.querySelectorAll(".gym-card").forEach((card) => {
    card.style.cursor = "pointer";
    card.addEventListener("click", function (e) {
      if (e.target.closest(".view-gym-btn")) return;

      const gymId = this.getAttribute("data-gym-id");
      window.loadGymDetail(gymId);
    });
  });

  document.querySelectorAll(".view-gym-btn").forEach((btn) => {
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      const gymId = this.getAttribute("data-gym-id");
      window.loadGymDetail(gymId);
    });
  });
}

function extractCityFromAddress(address) {
  const parts = address.split(",");
  if (parts.length >= 2) {
    return parts[parts.length - 2].trim();
  }
  return address;
}
