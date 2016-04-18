var drone_marker;

function initMap() 
{
    var mapDiv = document.getElementById('map');

    var position = {lat: 46.518524, lng: 6.567319};

    var map = new google.maps.Map(mapDiv, {
        center: position,
        scrollwheel: true,
        mapTypeId: google.maps.MapTypeId.SATELLITE,
        streetViewControl: false,
        zoom: 18
        });

    google.maps.event.addListener(map, 'click', function (e) {
        click_cb(e.latLng.lat(), e.latLng.lng());
    });

    var image = {
        url: 'static/js/images/quadcopter_icon.png',
        size: new google.maps.Size(100, 100),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(40, 40)
        };


    drone_marker = new google.maps.Marker({
        position: position,
        map: map,
        title: 'Drone',
        icon: image,
        draggable: true
        });
}

function click_cb(lat, lng)
{
    alert("Latitude: " + lat + "\r\nLongitude: " +lng);
}

function set_drone_pos(lat, lng)
{
    drone_marker.setPosition({lat: lat, lng: lng});
}
