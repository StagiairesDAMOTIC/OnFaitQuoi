let allActivities = [];
let map;
let userPosition = { lat: 0, lng: 0 };
let customTime = null;

const cityLocations = {
  city1: { lat: 43.3075, lng: 6.6378 }, // Sainte-Maxime
  city2: { lat: 43.5789, lng: 7.1285 }, // Ville 2 (exemple)
};

function findMe() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition((position) => {
      userPosition = {
        lat: position.coords.latitude,
        lng: position.coords.longitude,
      };
      showPosition(userPosition);
    }, showError);
  } else {
    alert("La géolocalisation n'est pas supportée par ce navigateur.");
  }
}

function updateLocation() {
  const locationSelect = document.getElementById("location-select").value;
  if (locationSelect === "current") {
    findMe();
  } else {
    userPosition = cityLocations[locationSelect];
    showPosition(userPosition);
  }
}

function updateTime() {
  const timeSelect = document.getElementById("time-select").value;
  const customTimeInput = document.getElementById("custom-time");
  if (timeSelect === "now") {
    customTime = null;
    customTimeInput.style.display = "none";
    filterByCategory();
  } else {
    customTimeInput.style.display = "inline";
  }
}

function updateCustomTime() {
  const customTimeInput = document.getElementById("custom-time").value;
  const [hours, minutes] = customTimeInput.split(":");
  customTime = new Date();
  customTime.setHours(hours);
  customTime.setMinutes(minutes);
  filterByCategory();
}

function showPosition(position) {
  var mapOptions = {
    center: position,
    zoom: 15,
  };

  map = new google.maps.Map(document.getElementById("map"), mapOptions);
  var marker = new google.maps.Marker({
    position: position,
    map: map,
    title: "Vous êtes ici",
  });

  fetch("activities.json")
    .then((response) => response.json())
    .then((data) => {
      allActivities = data.map((activity) => {
        activity.distance = getDistance(
          position.lat,
          position.lng,
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
  const now = customTime || new Date();
  const day = now.toLocaleString("en-us", { weekday: "long" });
  const [openHour, openMinute] = activity.opening_hours[day].open
    .split(":")
    .map(Number);
  const [closeHour, closeMinute] = activity.opening_hours[day].close
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

function toggleMenu() {
  const selector = document.querySelector(".selector");
  selector.style.display = selector.style.display === "flex" ? "none" : "flex";
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
