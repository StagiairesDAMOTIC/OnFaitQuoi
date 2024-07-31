let allActivities = [];
let map;

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
    zoom: 15,
  };

  map = new google.maps.Map(document.getElementById("map"), mapOptions);
  var marker = new google.maps.Marker({
    position: location,
    map: map,
    title: "Vous êtes ici",
  });

  fetch("activities.json")
    .then((response) => response.json())
    .then((data) => {
      allActivities = data.map((activity) => {
        activity.distance = getDistance(
          lat,
          lng,
          activity.latitude,
          activity.longitude
        );
        activity.isOpen = isOpen(activity);
        return activity;
      });
      filterByCategory();
    });
}

function getDistance(lat1, lon1, lat2, lon2) {
  const R = 6371; // Radius of the earth in km
  const dLat = deg2rad(lat2 - lat1);
  const dLon = deg2rad(lon2 - lon1);
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(deg2rad(lat1)) *
      Math.cos(deg2rad(lat2)) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  const distance = R * c; // Distance in km
  return distance;
}

function deg2rad(deg) {
  return deg * (Math.PI / 180);
}

function isOpen(activity) {
  const now = new Date();
  const [openHour, openMinute] = activity.opening_hours.open
    .split(":")
    .map(Number);
  const [closeHour, closeMinute] = activity.opening_hours.close
    .split(":")
    .map(Number);
  const openTime = new Date(
    now.getFullYear(),
    now.getMonth(),
    now.getDate(),
    openHour,
    openMinute
  );
  const closeTime = new Date(
    now.getFullYear(),
    now.getMonth(),
    now.getDate(),
    closeHour,
    closeMinute
  );
  return now >= openTime && now <= closeTime;
}

function filterByCategory() {
  const category = document.getElementById("category-select").value;
  let filteredActivities = allActivities;

  if (category !== "all") {
    filteredActivities = allActivities.filter(
      (activity) => activity.category === category
    );
  }

  displayActivities(filteredActivities);
}

function displayActivities(activities) {
  const sortedActivities = activities.sort((a, b) => {
    if (a.isOpen && !b.isOpen) return -1;
    if (!a.isOpen && b.isOpen) return 1;
    return a.distance - b.distance;
  });

  var placesList = document.getElementById("places");
  placesList.innerHTML = "";
  sortedActivities.forEach((activity) => {
    let placeBox = document.createElement("div");
    placeBox.classList.add("place-box");
    placeBox.innerHTML = `
            <p><strong>${activity.name}</strong></p>
            <p>Catégorie: ${activity.category}</p>
            <p>${activity.distance.toFixed(2)} km</p>
            <p>${activity.isOpen ? "Ouvert" : "Fermé"}</p>
        `;
    placeBox.addEventListener("click", () => {
      map.setCenter(
        new google.maps.LatLng(activity.latitude, activity.longitude)
      );
      map.setZoom(15);
    });
    placesList.appendChild(placeBox);
    new google.maps.Marker({
      position: { lat: activity.latitude, lng: activity.longitude },
      map: map,
      title: activity.name,
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
