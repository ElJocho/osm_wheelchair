let map = L.map('map_div', {
    zoom: 2,
    minZoom: 1,
    maxZoom: 12,
    center: [15.0, 15.0],
    maxBounds: [
        [-90, -180],
        [90, 180]
    ],
  });

  function initMap(map) {

    // load geojson file
    /*let list = new get_html_parameter_list(location.search)
    let loc = list["location"]
    if (loc === undefined){
        loc="heidelberg"
    }
    */
    L.tileLayer( 'https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png', {
    attribution: 'Map tiles by <a href="https://carto.com/">Carto</a>, under <a href="https://creativecommons.org/licenses/by/3.0/">CC BY 3.0.</a> Data by <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>, under ODbL.',
    }).addTo( map );

    //pois = "api/export/".concat(loc, "/project_activity_sessions_per_month.geojson");
    setTimeout(function(){ map.invalidateSize()}, 0);
    //addGeojsonLayer(map, pois);
    
    // add scale bar
    var scale = L.control.scale(
      {
        'imperial': false,
        'updateWhenIdle': true
      }
    );
    console.log("yeeehaw")

    scale.addTo(map);
  }
  initMap(map)
  
  function set_style_activity(feature) {
    if (feature.properties.status == "yes") {
        return {
        fillColor:  '#32a846',
        radius: 10}
    } else if (feature.properties.status == "no") {
        return {
        fillColor:  '#f22000',
        radius: 10}

    } else if (feature.properties.status == "limited") {
        return {
        fillColor:  '#ff7d03',
        radius: 10}

    }
}

