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
    let list = new get_html_parameter_list(location.search)
    let loc = list["location"]
    if (loc === undefined){
        loc="heidelberg"
    }
    
    let area_of_interest = "data/geojson/".concat(loc, ".geojson")
    addGeojsonLayer(map, area_of_interest);

    //let pois = "api/export/".concat(loc, "/project_activity_sessions_per_month.geojson");
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

function addGeojsonLayer (map, url) {

    try{
        map.eachLayer(function (layer) {

        map.removeLayer(layer);
    });
    }
    catch{
        console.log("nothing to catch")
    }

    L.tileLayer( 'https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png', {
        attribution: 'Map tiles by <a href="https://carto.com/">Carto</a>, under <a href="https://creativecommons.org/licenses/by/3.0/">CC BY 3.0.</a> Data by <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>, under ODbL.',
    }).addTo( map );

    var geojsonData = $.ajax({
        url:url,
        dataType: "json",
        success: console.log("geojson data successfully loaded."),
        error: function (xhr) {
        alert(xhr.statusText)
        }
    })
    // Specify that this code should run once the county data request is complete
    /*$.when(geojsonData).done(function() {
        // define default point style
        var geojsonMarker = {
            radius: 6,
            fillColor: "grey",
            color: "white",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8
        };
    */
        // create geojson layer
        // classification layer
        layer = L.geoJSON(geojsonData.responseJSON, {
            pointToLayer: function (feature, latlng) {
                let marker = L.circleMarker(latlng, geojsonMarker);
                marker.on("click", function(data) {
                    circleMarkerClick(data, map)
                });
                return marker;
            }        
            }).addTo(map)
        

  }
  