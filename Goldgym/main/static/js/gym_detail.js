function loadGymDetail(gymId) {
    fetch(`/gym-detail/${gymId}/`)
        .then(response => response.json())
        .then(gym => {
            document.getElementById('detail-gym-name').textContent = gym.name;
            document.getElementById('detail-gym-address').textContent = gym.address;
            document.getElementById('detail-gym-distance').textContent = gym.distance + " miles away";

            const img = document.getElementById('detail-gym-image');
            img.src = gym.image_url || '/static/img/noimage.jpg';
            img.alt = gym.name;

            const amenitiesList = document.getElementById('detail-gym-amenities');
            amenitiesList.innerHTML = '';
            gym.amenities.forEach(item => {
                const li = document.createElement('li');
                li.innerHTML = `✓ ${item.trim()}`;
                amenitiesList.appendChild(li);
            });

            document.getElementById('detail-opening-hours-weekdays').textContent = gym.opening_hours_weekdays;
            document.getElementById('detail-opening-hours-saturday').textContent = gym.opening_hours_saturday;
            document.getElementById('detail-opening-hours-sunday').textContent = gym.opening_hours_sunday;
            document.getElementById('detail-gym-phone').textContent = gym.phone;
            document.getElementById('detail-gym-email').textContent = gym.email;

            // Показываем детали
            document.getElementById('gym-list').style.display = 'none';
            document.getElementById('gym-detail').style.display = 'block';
        })
        .catch(error => {
            console.error('Помилка при завантаженні деталей спортзалу:', error);
        });
}

window.loadGymDetail = loadGymDetail;
