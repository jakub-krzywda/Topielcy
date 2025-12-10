var map = L.map('map').setView([51.505, -0.09], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var polyline = null;
var marker = null;

function updateMap() {
    fetch('/api/gps/')
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            if (!Array.isArray(data) || data.length === 0) {
                return;
            }

            var last = data[data.length - 1];
            if (!Array.isArray(last.latitude) || !Array.isArray(last.longitude)) {
                return;
            }

            var latlngs = [];
            var length = Math.min(last.latitude.length, last.longitude.length);

            for (var i = 0; i < length; i++) {
                latlngs.push([last.latitude[i], last.longitude[i]]);
            }

            if (latlngs.length === 0) {
                return;
            }

            if (polyline) {
                polyline.setLatLngs(latlngs);
            } else {
                polyline = L.polyline(latlngs, { color: 'red' }).addTo(map);
            }

            map.fitBounds(polyline.getBounds());

            var lastPoint = latlngs[latlngs.length - 1];
            if (marker) {
                marker.setLatLng(lastPoint);
            } else {
                marker = L.marker(lastPoint).addTo(map);
            }
        })
        .catch(function (error) {
            console.error('Error loading GPS data', error);
        });
}

updateMap();
setInterval(updateMap, 1000);