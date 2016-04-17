function initMap() 
{
    var mapDiv = document.getElementById('map');

    var map = new google.maps.Map(mapDiv, {
        center: {lat: 46.518524, lng: 6.567319},
        scrollwheel: true,
        mapTypeId: google.maps.MapTypeId.SATELLITE,
        streetViewControl: false,
        zoom: 18
        });

    google.maps.event.addListener(map, 'click', function (e) {
        alert("Latitude: " + e.latLng.lat() + "\r\nLongitude: " + e.latLng.lng());
        // sendPos(e.latLng.lat(), e.latLng.lng());
    });
}

function set_drone_pos(lat, long)
{
    alert('drone is in lat ' + String(lat) + ', long : ' + String(long));
}

// function sendPos(lat, long)
// {
// // var postdata = {"lat":lat};
// // $.post("/GET", postdata);


// // post the form values via AJAX…
//     var postdata = {lat: lat} ;
//     $.post('/GET', postdata);

//     alert("latitude sent");
// }