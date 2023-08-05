Chart.defaults.global.defaultFontFamily = '"Rubik", "Helvetica", "Arial", sans-serif';
Chart.defaults.global.responsive = true;
Chart.defaults.global.maintainAspectRatio = false;

var chart = null;

eel.expose(init_chart);
function init_chart(title, jsonstr, options) {
    // Set title
    document.title = title;

    // Get graph canvas context
    var ctx = document.getElementById("graph-canvas").getContext("2d");
    // Load chart data
    var chartData = JSON.parse(jsonstr);
    chartData.options = {...chartData.options, ...options}
    console.log(chartData);
    // Create chart
    chart = new Chart(ctx, chartData);
}

eel.expose(update_chart);
function update_chart(jsonstr) {
    // Load new chart data
    var chartData = JSON.parse(jsonstr);
    for (var i = 0; i < chart.data.datasets.length; i++) {
        // update the data
        chart.data.datasets[i].data = chartData.data.datasets[i].data;
        chart.data.datasets[i].backgroundColor = chartData.data.datasets[i].backgroundColor;
        chart.data.datasets[i].borderColor = chartData.data.datasets[i].borderColor;
    }
    // update the data labels
    chart.data.labels = chartData.data.labels;

    console.log(chartData);
    chart.update();
}
