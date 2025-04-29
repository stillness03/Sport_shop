document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('gym-search').addEventListener('input', function(e) {
        const searchTerm = e.target.value.toLowerCase();
        const gymCards = document.querySelectorAll('.gym-card');

        gymCards.forEach(card => {
            const gymText = card.textContent.toLowerCase();
            if (gymText.includes(searchTerm)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });

    document.getElementById('gym-list').addEventListener('click', function (e) {
        const card = e.target.closest('.gym-card');
        if (card) {
            const gymId = card.getAttribute('data-gym-id');
            loadGymDetail(gymId);
        }
    });

    document.getElementById('back-to-list').addEventListener('click', function() {
        document.getElementById('gym-detail').style.display = 'none';
    });

    function loadGymDetail(gymId) {
        const card = document.querySelector(`.gym-card[data-gym-id="${gymId}"]`);

        const gym = {
            name: card.getAttribute('data-name'),
            address: card.getAttribute('data-address'),
            distance: card.getAttribute('data-distance'),
            amenities: card.getAttribute('data-amenities').split(','),
            hours: card.getAttribute('data-hours'),
            imageUrl: card.getAttribute('data-image-url')
        };

        document.getElementById('detail-gym-name').textContent = gym.name;
        document.getElementById('detail-gym-address').textContent = gym.address;
        document.getElementById('detail-gym-distance').textContent = gym.distance + " miles away";

        const img = document.getElementById('detail-gym-image');
        img.src = gym.imageUrl || '/static/img/noimage.jpg';
        img.alt = gym.name;

        const amenitiesList = document.getElementById('detail-gym-amenities');
        amenitiesList.innerHTML = '';
        gym.amenities.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            amenitiesList.appendChild(li);
        });

        document.getElementById('detail-gym-hours').textContent = gym.hours;
        document.getElementById('gym-list').style.display = 'none';
        document.getElementById('gym-detail').style.display = 'block';
    }
});