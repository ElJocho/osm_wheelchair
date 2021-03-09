function setLinePlot(name, input_sl, data, yaxis) {

    var layout = {
    title: name,
    xaxis: {
        type: "date",
        dtick:"M12",
        fixedrange: true,
        automargin:true
    },
    yaxis: {
        fixedrange: true,
        title: yaxis,
        tickformat: '.2f',
        automargin:true
    },
    legend: {
        y:1,
        x:0.1
    },
    margin: {
        l: 50,
        r: 50,
        b: 50,
        t: 50,
        pad: 4
    }
    };

    Plotly.newPlot(input_sl, data, layout, {displayModeBar: false, responsive: true});
};


function plot_key_progress() {

    let list = new get_html_parameter_list(location.search)
    let aoi = list["aoi"]
    if (aoi === undefined){
      aoi="area_of_interest"
    }
  
    let time_series_path = "data/result/".concat(aoi, "/time_series.json")

    let t_data = get_json(time_series_path);

    let x_t_data=Object.keys(t_data["tagging"]);
    x_t_data=x_t_data.map(function(x){
        return new Date(Math.round(x));
    })

    let y_yes_t_data=[]
    let y_no_t_data=[]
    let y_partial_t_data=[]

    
	for(var i=0; i<Object.keys(t_data["tagging"]).length; i++){
        y_yes_t_data.push(Object.values(t_data["tagging"])[i][0])
        y_no_t_data.push(Object.values(t_data["tagging"])[i][1])
        y_partial_t_data.push(Object.values(t_data["tagging"])[i][2])
    }

    let yes={
        x: x_t_data,
        y: y_yes_t_data,
        type: "line",
        name:"wheelchair=yes",
        marker:{
        color: "green"
        }
    };
    let no={
        x: x_t_data,
        y: y_no_t_data,
        type: "line",
        name:"wheelchair=no",
        marker:{
        color: "red"
        }
    };
    let partial={
        x: x_t_data,
        y: y_partial_t_data,
        type: "line",
        name:"wheelchair=partial",
        marker:{
        color: "yellow"
        }
    };
    let input = document.getElementById("time_series")
    let data = [yes, no , partial]

    setLinePlot("Evolution of wheelchair tags for amenities over time", input, data, "total number")

}


function tag_progress() {

    let list = new get_html_parameter_list(location.search)
    let aoi = list["aoi"]
    if (aoi === undefined){
      aoi="area_of_interest"
    }
  
    let time_series_path = "data/result/".concat(aoi, "/share_tags.json")

    let tag_data = get_json(time_series_path);

    let x_tag_data=Object.keys(tag_data["share_tagged"]);
    x_tag_data=x_tag_data.map(function(x){
        return new Date(Math.round(x));
    })


    
    let y_tag_data=Object.values(tag_data["share_tagged"]);

    let share={
        x: x_tag_data,
        y: y_tag_data,
        type: "line",
        name:"share tagged",
        marker:{
        color: "green"
        }
    };
    let input_tags = document.getElementById("share_tagged")
    let data_tags = [share]

    setLinePlot("Evolution of relevant roads tags over time", input_tags, data_tags, "share of roads (in %)")

}
