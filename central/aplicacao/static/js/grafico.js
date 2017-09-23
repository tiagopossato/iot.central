var initGrafico = function () {
    var data = [];
    var layout = {
        legend: {
            orientation: 'h',
            yanchor: 'top',
            xanchor: 'left'
        },
        showlegend: true
    };

    var dialog = bootbox.dialog({
        message: '<p class="text-center"><i class="fa fa-spin fa-spinner"></i></p><p class="text-center">Buscando dados...</p>',
        closeButton: false,
        size: 'small'
    });

    $.get(location.protocol + "//" + location.host + "/app/leituras", function (data, status) {

        data.forEach(function (sensor) {
            // console.log(sensor)
            sensor.g.forEach(function (grandeza) {
                var trace = {
                    x: [],
                    y: [],
                    type: 'scatter',
                    name: sensor.d + ' [' + grandeza.n + ']'
                }
                grandeza.l.forEach(function (leitura) {
                    // console.log(leitura)
                    trace.y.push(leitura.v);
                    trace.x.push(leitura.c);
                }, this);
                data.push(trace);
            }, this);
        }, this);
        dialog.modal('hide');
        Plotly.newPlot('grafico', data, layout);
    });

}