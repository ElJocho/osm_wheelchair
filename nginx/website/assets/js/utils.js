
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
  


function update_url(param, value){
	let new_params = "?" + param + "=" + value
	window.history.replaceState(null, null, new_params);
}
  