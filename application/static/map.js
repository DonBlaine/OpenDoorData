var map;
var marker;

function initialize() {
	var mapProp = {
		center: new google.maps.LatLng(53.3075343,-6.2215082),
		zoom: 16,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	};
	map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
}

google.maps.event.addDomListener(window, 'load', initialize);

function addMarker(lat, lng){
	var marker = new google.maps.Marker({
    position: new google.maps.LatLng(53.3092327,-6.2239067),
    title:"Hello World!"
});

	marker.setMap(map);
	map.setCenter(new google.maps.LatLng(53.3092327,-6.2239067));
}
