function loadGymDetail(gymId) {
  fetch(`/gym-detail/${gymId}/`)
    .then((response) => response.json())
    .then((gym) => {
      document.getElementById("detail-gym-name").textContent = gym.name;
      document.getElementById("detail-gym-address").textContent = gym.address;
      if (gym.latitude && gym.longitude) {
        const center = map.getCenter();
        const distanceInKm = Math.round(
          center.distanceTo(L.latLng(gym.latitude, gym.longitude)) / 1000
        );
        document.getElementById(
          "detail-gym-distance"
        ).textContent = `${distanceInKm} km away`;
      } else {
        document.getElementById(
          "detail-gym-distance"
        ).textContent = `Location not available`;
      }
      const statusBadge = document.getElementById("detail-gym-status");
      if (gym.status) {
        statusBadge.textContent = "OPEN";
        statusBadge.className = "badge border border-success text-success";
      } else {
        statusBadge.textContent = "CLOSED";
        statusBadge.className = "badge border border-danger text-danger";
      }

      const galleryContainer = document.getElementById("gym-additional-images");
      galleryContainer.innerHTML = "";

      if (gym.additional_images && gym.additional_images.length > 0) {
        gym.additional_images.slice(0, 4).forEach((imageUrl) => {
          const imgWrapper = document.createElement("div");
          imgWrapper.className = "me-2 flex-shrink-0";
          imgWrapper.style.width = "140px";

          const img = document.createElement("img");
          img.src = imageUrl;
          img.alt = gym.name + " gallery image";
          img.className = "img-fluid rounded h-100";
          img.style.objectFit = "cover";
          img.style.cursor = "pointer";

          imgWrapper.appendChild(img);
          galleryContainer.appendChild(imgWrapper);
        });
      } else {
        galleryContainer.innerHTML =
          '<p class="text-muted">No additional images available</p>';
      }

      const amenitiesList = document.getElementById("detail-gym-amenities");
      amenitiesList.innerHTML = "";
      gym.amenities.forEach((item) => {
        const li = document.createElement("li");
        li.innerHTML = `✓ ${item.trim()}`;
        amenitiesList.appendChild(li);
      });

      document.getElementById("detail-opening-hours-weekdays").textContent =
        gym.opening_hours_weekdays;
      document.getElementById("detail-opening-hours-saturday").textContent =
        gym.opening_hours_saturday;
      document.getElementById("detail-opening-hours-sunday").textContent =
        gym.opening_hours_sunday;
      document.getElementById("detail-gym-phone").textContent = gym.phone;
      document.getElementById("detail-gym-email").textContent = gym.email;

      document.getElementById("gym-list").style.display = "none";
      document.getElementById("gym-detail").style.display = "block";
    });
}

window.loadGymDetail = loadGymDetail;
