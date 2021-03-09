function update_map(){

  document.getElementById('map_div').innerHTML = "<div id='map' class='map'></div>";
  let map = L.map('map')

  var info = L.control();

  info.onAdd = function (map) {
      this._div = L.DomUtil.create('div', 'info');
      this.update();
      return this._div;
  };

  function get_tags(props){
    value = "";
    (props.highway!=undefined) ? value += '<p>type of street: ' + props.highway + '</p>' : value+="";
    (props.smoothness!=undefined) ? value += '<p>smoothness: ' + props.smoothness + '</p>'  : value+="";
    (props.surface!=undefined) ? value += '<p>surface: ' + props.surface + '</p>'  : value+="";
    (props.incline!=undefined) ? value += '<p>' + props.incline + '% incline </p>' : value+="";
    (props.sidewalk!=undefined) ? value += '<p>sidewalk on ' + props.sidewalk + ' side(s)</p>'  : value+="";
    return value
  }

  info.update = function (props) {

      this._div.innerHTML = '<h4>Road Characteristics</h4>' +  (props ?
          '<p><b>Score: '+ props.wheelchair_score + '</b></p>' +
          '<p>' + props.wheelchair_tags + ' wheelchair tags </p>' +
          get_tags(props)


          : '<p>Hover over a Road') 
  };

  info.addTo(map);

  function highlightFeature(e) {
    var Layer = e.target;

    Layer.setStyle({
        opacity: 1,
        weight: 5,
    });

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        Layer.bringToFront();
    }
    info.update(Layer.feature.properties);
  }

  function resetHighlight(e) {
      var Layer = e.target;
      layer.resetStyle(e.target);
      info.update();
  }

  function onEachFeature(feature, layer) {
      layer.on({
          mouseover: highlightFeature,
          mouseout: resetHighlight,
      });
  }





    function initMap(map) {

      // load geojson file
      let list = new get_html_parameter_list(location.search)
      let aoi = list["aoi"]
      if (aoi === undefined){
        aoi="area_of_interest"
      }
    
      let aoi_path = "data/areas_of_interest/".concat(aoi, ".geojson")
      let roads = "data/result/".concat(aoi, "/roads_geoms.geojson")
      road_data = get_json(roads)
      aoi_data = get_json(aoi_path)
      aoi_layer = L.geoJSON(aoi_data)
      map.fitBounds(aoi_layer.getBounds());

      addGeojsonLayer(map, road_data);

      setTimeout(function(){ map.invalidateSize()}, 0);
      
      // add scale bar
      var scale = L.control.scale(
        {
          'imperial': false,
          'updateWhenIdle': true
        }
      );
      scale.addTo(map);
    }
    initMap(map)
    
    function style(feature) {
      if (feature.properties.wheelchair_score >=0.7 & feature.properties.wheelchair_score <=1) {
          return {
          color:  '#00c700',
          }
      } else if (feature.properties.wheelchair_score >= 0 &feature.properties.wheelchair_score <0.7) {
          return {
          color:  '#f3c81b'
          }
      } else if (feature.properties.wheelchair_score >= -1 & feature.properties.wheelchair_score < 0){
          return {
          color:  '#ff0000',
          }

      } else if (feature.properties.wheelchair_score == -2){
          return {
          color:  '#000000',
          }

      }
  }

  var legend = L.control({position: 'bottomright'});

  legend.onAdd = function (map) {

      var div = L.DomUtil.create('div', 'info legend');

      grades = ['#000000','#ff0000', '#f3c81b', '#00c700'];
      labels = ["No Data", "mainly bad", "neutral", "good"];

      for (var i = 0; i < grades.length; i++) {
          div.innerHTML +=
              '<i style="background:' + grades[i] + '"></i> ' +
              labels[i] + ' </br> ';
  }

  return div;
  };

  legend.addTo(map);

  function addGeojsonLayer (map, data) {

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


      layer = L.geoJSON(data, {style: style, onEachFeature:onEachFeature}).addTo(map)
      return layer

    }
    

}