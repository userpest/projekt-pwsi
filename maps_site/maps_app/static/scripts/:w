var map;

/* Create the map */
$(document).ready(
function(){
  map = new GMaps({
    div: '#the_map',
    lat: -12.043333,
    lng: -77.028333
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
            draggable: true
        });
    };
}
