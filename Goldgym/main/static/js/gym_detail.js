function loadGymDetail(gymId) {
  fetch(`/gym-detail/${gymId}/`)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then((gym) => {
      document.getElementById("detail-gym-name").textContent = gym.name || "No name provided";
      document.getElementById("detail-gym-address").textContent = gym.address || "No address available";

      const distanceEl = document.getElementById("detail-gym-distance");
      if (gym.latitude && gym.longitude && typeof map !== "undefined") {
        const center = map.getCenter();
        const distanceInKm = Math.round(center.distanceTo(L.latLng(gym.latitude, gym.longitude)) / 1000);
        distanceEl.textContent = `${distanceInKm} km away`;
      } else {
        distanceEl.textContent = `Location not available`;
      }

      const statusBadge = document.getElementById("detail-gym-status");
      const isOpen = Boolean(gym.status);
      statusBadge.textContent = isOpen ? "OPEN" : "CLOSED";
      statusBadge.className = isOpen
        ? "badge border border-success text-success"
        : "badge border border-danger text-danger";

      const galleryContainer = document.getElementById("gym-additional-images");
      galleryContainer.innerHTML = "";

      if (Array.isArray(gym.additional_images) && gym.additional_images.length > 0) {
        gym.additional_images.slice(0, 4).forEach((imageUrl) => {
          const wrapper = document.createElement("div");
          wrapper.className = "me-2 flex-shrink-0";
          wrapper.style.width = "140px";

          const img = document.createElement("img");
          img.src = imageUrl;
          img.alt = `${gym.name} gallery image`;
          img.className = "img-fluid rounded h-100";
          img.style.objectFit = "cover";
          img.style.cursor = "pointer";

          wrapper.appendChild(img);
          galleryContainer.appendChild(wrapper);
        });
      } else {
        galleryContainer.innerHTML = '<p class="text-muted">No additional images available</p>';
      }

      const amenitiesList = document.getElementById("detail-gym-amenities");
      amenitiesList.innerHTML = "";
      (gym.amenities || []).forEach((item) => {
        const li = document.createElement("li");
        li.textContent = `✓ ${item.trim()}`;
        amenitiesList.appendChild(li);
      });

      document.getElementById("detail-opening-hours-weekdays").textContent = gym.opening_hours_weekdays || "-";
      document.getElementById("detail-opening-hours-saturday").textContent = gym.opening_hours_saturday || "-";
      document.getElementById("detail-opening-hours-sunday").textContent = gym.opening_hours_sunday || "-";

      document.getElementById("detail-gym-phone").textContent = gym.phone || "-";
      document.getElementById("detail-gym-email").textContent = gym.email || "-";

      document.getElementById("gym-list").style.display = "none";
      document.getElementById("gym-detail").style.display = "block";
    })
    .catch((error) => {
      console.error("Error loading gym details:", error);
      alert("Failed to load gym details. Please try again later.");
    });
}

window.loadGymDetail = loadGymDetail;
