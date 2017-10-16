var initGrafico = function () {
    var linhas = [];
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

    $.get(window.location.origin + "/app/leituras", function (data, status) {

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
                    // console.log(leitura);
                    //grafico do valor
                    trace.y.push(leitura.v);
                    trace.x.push(new Date(leitura.c * 1000));
                }, this);
                linhas.push(trace);
            }, this);
        }, this);
        dialog.modal('hide');
        Plotly.newPlot('grafico', linhas, layout);
    });

}