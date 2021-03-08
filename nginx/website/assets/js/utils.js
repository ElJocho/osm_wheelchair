
function get_json(src) {
	var data_dict = null;
	$.ajax({
		'async': false,
		'global': false,
		'url': src,
		'dataType': "json",
		'success': function(data) {
			data_dict = data;
		}
	});
	return data_dict;
}


function get_html_parameter_list(querystring) {
	if (querystring == '') return;
	var params = querystring.slice(1);
	var pairs = params.split("&");
	var pair, name, value;
	for (var i = 0; i < pairs.length; i++) {
		pair = pairs[i].split("=");
		name = pair[0];
		value = pair[1];
		name = unescape(name).replace("+", " ");
		value = unescape(value).replace("+", " ");
		this[name] = value;
	}
	return this
}
  
function get_directories(){
	data = get_json("data/result/valid_dirs.json")
	return data["dirs"]
}

function update_url(param, value){
	let new_params = "?" + param + "=" + value
	window.history.replaceState(null, null, new_params);
}

function update_function_caller(functions){
	for(let i=0; i<functions.length; i++){
	  functions[i]()
	}
  }
  
  function fill_aoi_dropdown(functions){
	let aoi;
	if(location.search == ''){
	  aoi = "area_of_interest"
	}
	else{
	  let list = get_html_parameter_list(location.search)
	  aoi = list["aoi"]
	}

	let entries = get_directories();
	var x = document.getElementById("aois");
	for(var i=0; i<Object.keys(entries).length; i++){
	  var option = document.createElement("option");
	  option.text=Object.values(entries)[i]
	  option.value=Object.values(entries)[i]
	  if (option.text === aoi){
		option.setAttribute("selected", true)
	  }
	  x.add(option)
	}
	x.value = aoi
  
	var val = $("#aois").val();
	$("#aois").prepend("<option value='" + val + "' data-value='selected' selected hidden>" + val + "</option>");
  
	$("#aois").on('change', function() {
	  var val = $("#aois").val();
  
	  $("#aois option[data-value='selected']").attr('value', val);
	  $("#aois option[data-value='selected']").text(val);
	  $("#aois").val(val);
	});

	$(x).on("change", function(){
	  update_url("aoi", this.value)
	  update_function_caller(functions)
	})

  }