function plot_key_progress() {
    let data_progress = get_json("data/result".concat("/example2.json"));


    let x_data_progress=Object.keys(data_progress["hex_cum_contributions_added"]);
    x_data_progress=x_data_progress.map(function(x){
        return new Date(Math.round(x));
    })

    let y_data_progress=Object.values(data_progress["hex_cum_contributions_added"]);

    let contributions={
        x: x_data_progress,
        y: y_data_progress,
        type: "line",
        name:"Contributions over time",
        marker:{
        color: "red"
        }
    };
    let input_progress = document.getElementById("progress")


    function setLinePlot(name, input_sl, data) {

        var layout = {
        title: name,
        xaxis: {
            type: "date",
            dtick:"M12",
            fixedrange: true
        },
        yaxis: {
            fixedrange: true,
            title: "share work done",
            tickformat: '.2f'
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

        Plotly.newPlot(input_sl, [data], layout, {displayModeBar: false, responsive: true});
    };
    setLinePlot("Progress", input_progress, contributions)

}
plot_key_progress()