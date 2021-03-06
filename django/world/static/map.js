const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors';
const map = L.map('map').setView([50.2858, 20.78682], 5);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: attribution}).addTo(map);

L.control.scale().addTo(map);

const provider = new GeoSearch.EsriProvider();
// const provider = new GeoSearch.OpenStreetMapProvider();

const searchControl = new GeoSearch.GeoSearchControl({
    provider: provider,
    style: 'bar',
    // howMarker: true, // optional: true|false  - default true
    // showPopup: false, // optional: true|false  - default false
    // marker: {
    //     // optional: L.Marker    - default L.Icon.Default
    //     icon: new L.Icon.Default(),
    //     draggable: false,
    // },
    // popupFormat: ({query, result}) => result.label, // optional: function    - default returns result label,
    // resultFormat: ({result}) => result.label, // optional: function    - default returns result label
    // maxMarkers: 1, // optional: number      - default 1
    // retainZoomLevel: false, // optional: true|false  - default false
    // animateZoom: true, // optional: true|false  - default true
    // autoClose: false, // optional: true|false  - default false
    // searchLabel: 'Enter address', // optional: string      - default 'Enter address'
    // keepResult: false, // optional: true|false  - default false
    // updateMap: true, // optional: true|false  - default true
});


map.addControl(searchControl);

map.on('click', function (e) {
    map.dragging.enable();
    map.touchZoom.enable();
    map.doubleClickZoom.enable();
    map.scrollWheelZoom.enable();
    map.boxZoom.enable();
    map.keyboard.enable();
});

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
            if (data === "No region selected") {
                $("#modalCBody").html("Nie wybrano ??adnego obszaru");
                $(".modal-title").html("Ostrze??enie");
                $('#coordinatesModal').modal('show');
            } else if (data === "Select only one region") {
                $('#coordinatesModal').modal('show');
                $("#modalCBody").html("Zaznacz tylko jeden obszar.");
                $(".modal-title").html("Ostrze??enie");
            } else {
                $("#modalCBody").html(data);
                $(".modal-title").html("Wsp????rz??dne");
                $('#coordinatesModal').modal('show');
            }
        }
    });
}

function display_hypsometric() {
    var json_data = featureGroup.toGeoJSON();
    if (document.getElementById('smooth').checked) {
        json_data["smooth_color"] = 1;
    } else {
        json_data["smooth_color"] = 0;
    }

    if (document.getElementById('angle').value !== "") {
        json_data["angle"] = parseInt(document.getElementById('angle').value);
    } else {
        json_data["angle"] = 45;
    }
    if (document.getElementById('azimuth').value !== "") {
        json_data["azimuth"] = parseInt(document.getElementById('azimuth').value);
    } else {
        json_data["azimuth"] = 315;
    }

    var json_string = JSON.stringify(json_data);
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    $('#waitModal').modal('show');
    $.ajax({
        type: "POST",
        url: "/map/parse_coordinates_hypsometric",
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", csrftoken);
            request.setRequestHeader("Content-type", "application/json");
        },
        data: json_string,
        dataType: "text",
        mode: 'same-origin',
        success: function (data) {
            $('#waitModal').modal('hide');

            if (data === "No region selected") {
                $('#coordinatesModal').modal('show');
                $("#modalCBody").html("Najpierw zaznacz prostok??t na mapie.");
                $(".modal-title").html("Ostrze??enie");
            } else if (data === "Select only one region") {
                $('#coordinatesModal').modal('show');
                $("#modalCBody").html("Zaznacz tylko jeden obszar.");
                $(".modal-title").html("Ostrze??enie");
            } else if (data === "Wrong parameters") {
                $('#coordinatesModal').modal('show');
                $("#modalCBody").html("Niepoprawne parametry.");
                $(".modal-title").html("Ostrze??enie");
            } else {
                window.open("/map/display_hypsometric/" + data, '_blank');
            }
        }
    });
}

function display_3D() {
    var json_data = featureGroup.toGeoJSON();
    if (document.getElementById('smooth').checked) {
        json_data["smooth_color"] = 1;
    } else {
        json_data["smooth_color"] = 0;
    }

    var json_string = JSON.stringify(json_data);
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    $('#waitModal').modal('show');
    $.ajax({
        type: "POST",
        url: "/map/parse_coordinates_3D",
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", csrftoken);
            request.setRequestHeader("Content-type", "application/json");
        },
        data: json_string,
        dataType: "text",
        mode: 'same-origin',
        success: function (data) {
            $('#waitModal').modal('hide');

            if (data === "No region selected") {
                $('#coordinatesModal').modal('show');
                $("#modalCBody").html("Najpierw zaznacz prostok??t na mapie.");
                $(".modal-title").html("Ostrze??enie");
            } else if (data === "Select only one region") {
                $('#coordinatesModal').modal('show');
                $("#modalCBody").html("Zaznacz tylko jeden obszar.");
                $(".modal-title").html("Ostrze??enie");
            } else {
                window.open("/map/display_3d/" + data, '_blank');
            }
        }
    });
}
