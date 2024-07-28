function findMe() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError);
    } else {
        alert("La géolocalisation n'est pas supportée par ce navigateur.");
    }
}

function showPosition(position) {
    var lat = position.coords.latitude;
    var lng = position.coords.longitude;
    var location = new google.maps.LatLng(lat, lng);

    var mapOptions = {
        center: location,
        zoom: 15
    };

    var map = new google.maps.Map(document.getElementById("map"), mapOptions);
    var marker = new google.maps.Marker({
        position: location,
        map: map,
        title: "Vous êtes ici"
    });

    fetch('activities.json')
        .then(response => response.json())
        .then(data => {
            const sortedActivities = sortActivities(data, lat, lng);
            displayActivities(sortedActivities, map);
        });
}

function sortActivities(activities, userLat, userLng) {
    function getDistance(lat1, lon1, lat2, lon2) {
        const R = 6371; // Radius of the earth in km
        const dLat = deg2rad(lat2 - lat1);
        const dLon = deg2rad(lon2 - lon1);
        const a =
            Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        const distance = R * c; // Distance in km
        return distance;
    }

    function deg2rad(deg) {
        return deg * (Math.PI / 180);
    }

    function isOpen(activity) {
        const now = new Date();
        const [openHour, openMinute] = activity.opening_hours.open.split(':').map(Number);
        const [closeHour, closeMinute] = activity.opening_hours.close.split(':').map(Number);
        const openTime = new Date(now.getFullYear(), now.getMonth(), now.getDate(), openHour, openMinute);
        const closeTime = new Date(now.getFullYear(), now.getMonth(), now.getDate(), closeHour, closeMinute);
        return now >= openTime && now <= closeTime;
    }

    return activities.map(activity => {
        activity.distance = getDistance(userLat, userLng, activity.latitude, activity.longitude);
        activity.isOpen = isOpen(activity);
        return activity;
    }).sort((a, b) => {
        if (a.isOpen && !b.isOpen) return -1;
        if (!a.isOpen && b.isOpen) return 1;
        return a.distance - b.distance;
    });
}

function displayActivities(activities, map) {
    var placesList = document.getElementById('places');
    placesList.innerHTML = '';
    activities.forEach(activity => {
        placesList.innerHTML += `<p>${activity.name} - ${activity.distance.toFixed(2)} km - ${activity.isOpen ? 'Ouvert' : 'Fermé'}</p>`;
        new google.maps.Marker({
            position: { lat: activity.latitude, lng: activity.longitude },
            map: map,
            title: activity.name
        });
    });
}

function showError(error) {
    switch (error.code) {
        case error.PERMISSION_DENIED:
            alert("L'utilisateur a refusé la demande de géolocalisation.");
            break;
        case error.POSITION_UNAVAILABLE:
            alert("Les informations de localisation sont indisponibles.");
            break;
        case error.TIMEOUT:
            alert("La demande de localisation a expiré.");
            break;
        case error.UNKNOWN_ERROR:
            alert("Une erreur inconnue s'est produite.");
            break;
    }
}
