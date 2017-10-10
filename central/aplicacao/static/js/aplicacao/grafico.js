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
                    name: sensor.d + ' [' + grandeza.n + ']'                }
                var traceMV = {
                    x: [],
                    y: [],
                    type: 'scatter',
                    name: 'Media movel'
                }

                var traceFR = {
                    x: [],
                    y: [],
                    type: 'bar',
                    name: 'intervalo de leitura'
                }
                grandeza.l.forEach(function (leitura) {
                    // console.log(leitura);
                    valuePush(leitura.v, leitura.c);
                    var media = avgCalc();
                    traceMV.y.push(media);
                    traceMV.x.push(new Date(leitura.c * 1000));
                    var diferenca = Math.abs(leitura.v - media);
                    pcMovingAverage(diferenca);
                    trace.y.push(leitura.v);
                    trace.x.push(new Date(leitura.c * 1000));
                }, this);
                linhas.push(trace);
                linhas.push(traceMV);
            }, this);
        }, this);
        dialog.modal('hide');
        Plotly.newPlot('grafico', linhas, layout);
    });

}