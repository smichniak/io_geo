const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors';
const map = L.map('map').setView([50.2858, 20.78682], 5);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: attribution }).addTo(map);


var LeafIcon = L.Icon.extend({
  options: {
    shadowUrl:
        'http://leafletjs.com/docs/images/leaf-shadow.png',
    iconSize:     [38, 95],
    shadowSize:   [50, 64],
    iconAnchor:   [22, 94],
    shadowAnchor: [4, 62],
    popupAnchor:  [-3, -76]
  }
});

var greenIcon = new LeafIcon({
  iconUrl: 'http://leafletjs.com/docs/images/leaf-green.png'
  });

var drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

var drawControl = new L.Control.Draw({
  position: 'topright',
  draw: {
    polygon: {
      shapeOptions: {
        color: 'purple'
      },
      allowIntersection: false,
      drawError: {
        color: 'orange',
        timeout: 1000
      },
      showArea: true,
      metric: false,
      repeatMode: true
    },
    polyline: {
      shapeOptions: {
        color: 'red'
      },
    },
    rect: {
      shapeOptions: {
        color: 'green'
      },
    },
    circle: {
      shapeOptions: {
        color: 'steelblue'
      },
    },
    marker: {
      icon: greenIcon
    },
  },
  edit: {
    featureGroup: drawnItems
  }
});
map.addControl(drawControl);

map.on('draw:created', function (e) {
  var type = e.layerType,
    layer = e.layer;

  if (type === 'marker') {
    layer.bindPopup('A popup!');
  }

  drawnItems.addLayer(layer);
});
