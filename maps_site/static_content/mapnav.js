var map;
var icon = new google.maps.MarkerImage('http://static.dajaxproject.com/img/starpointer.png');

/* Create the map */
$(document).ready(function(){
  prettyPrint();
  map = new GMaps({
    div: '#the_map',
    lat: 37.413391,
    lng: -122.085013
  });

});

/* Draw points callback */
function example_draw_points(data){
    for (var i=0; i < data.length; i++) {
        map.addMarker({
            lat: data[i].lat,
            lng: data[i].lng,
            details: {id: i},
            dragend: function(e){
                Dajaxice.examples.move_point(Dajax.process,
                    {'lat':e.position.lat(),'lng':e.position.lng()});
            },
            draggable: true,
            icon: icon
        });
    };
}