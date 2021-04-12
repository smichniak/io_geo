const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors';
const map = L.map('map').setView([50.2858, 20.78682], 5);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: attribution}).addTo(map);

var featureGroup = L.featureGroup().addTo(map);

var drawControl = new L.Control.Draw({
    position: 'topright',
    edit: {
        featureGroup: featureGroup
    }
}).addTo(map);

map.on('draw:created', function (e) {
    // Each time a feature is created, it's added to the over arching feature group
    featureGroup.addLayer(e.layer);
});

function clear_regions() {
    featureGroup.clearLayers();
}

function send_data() {
    var json = JSON.stringify(featureGroup.toGeoJSON());
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    $('#coordinatesModal').modal('show');
    $.ajax({
        type: "POST",
        url: "/map/display_coordinates",
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", csrftoken);
            request.setRequestHeader("Content-type", "application/json");
        },
        data: json,
        dataType: "text",
        mode: 'same-origin',
        success: function (data) {
            // console.log(json);
            $("#modalCBody").html(data)
        }
    });
}

function display_hypsometric() {
    var json = JSON.stringify(featureGroup.toGeoJSON());
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    $.ajax({
        type: "POST",
        url: "/map/parse_coordinates_hypsometric",
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", csrftoken);
            request.setRequestHeader("Content-type", "application/json");
        },
        data: json,
        dataType: "text",
        mode: 'same-origin',
        success: function (data) {
            if (data === "No region selected") {
                $('#coordinatesModal').modal('show');
                $("#modalCBody").html("Najpierw zaznacz prostokąt na mapie.");
                $(".modal-title").html("Ostrzeżenie");
            } else if (data === "Select only one region") {
                $('#coordinatesModal').modal('show');
                $("#modalCBody").html("Zaznacz tylko jeden obszar.");
                $(".modal-title").html("Ostrzeżenie");
            } else {
                window.location.href = "/map/display_hypsometric/" + data;
            }
        }
    });
}

function display_3D() {
    var json = JSON.stringify(featureGroup.toGeoJSON());
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    $.ajax({
        type: "POST",
        url: "/map/parse_coordinates_3D",
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", csrftoken);
            request.setRequestHeader("Content-type", "application/json");
        },
        data: json,
        dataType: "text",
        mode: 'same-origin',
        success: function (data) {
            // This needs to be done yet.
            // window.location.href = "/map/display_3D";
        }
    });
}