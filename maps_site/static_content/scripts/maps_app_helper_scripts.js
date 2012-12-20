function save_coords(){
	center = window.myMap.getCenter();
	zoom = window.myMap.getZoom();
	Dajaxice.maps_app.save_coords(Dajax.process,{'lat':center.lat(), 'lng':center.lng(), 'zoom':zoom})

}

function set_location(data){
	newLatLng = new google.maps.LatLng(data.lat,data.lng);
	window.myMap.setCenter(newLatLng);
	if(data.hasOwnProperty("zoom")){
		window.myMap.setZoom(data.zoom);
	}
}

function send_form(e_id){
	sform = $('#share_saved_entry_form').serialize();
	//alert(sform);
	Dajaxice.maps_app.save_share_options( Dajax.process ,{ 
	'e_id':e_id,
	'input_form': sform,
	'container': 'share_saved_entry_form'
	});
}

var markers = {} ;
function add_marker(data){
	newLatLng = new google.maps.LatLng(data.lat,data.lng);
	mtitle = data.comment;
	marker = new google.maps.Marker({
		position : newLatLng,
		title : mtitle,
		map: window.myMap
	})
	marker_id = data.marker_id;
	markers[marker_id]=marker;

}

function remove_marker(data){
	marker_id = data.marker_id;	
	markers[marker_id].setMap(null);
	delete markers[marker_id];
}
