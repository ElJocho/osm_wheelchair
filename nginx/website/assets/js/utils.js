
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
