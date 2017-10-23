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
                    name: sensor.d + ' [' + grandeza.n + '](Intervalo de 1 min)'
                }

                /** VARIÁVEIS DO SENSOR */
                var frequenciaLeitura = 10;
                var freqMin = 10;
                var freqMax = 20;
                var seresta = new Seresta(freqMin, freqMax);

                /** FIM DAS VARIÁVEIS DO SENSOR */

                /** VARIÁVEIS DE TESTE */
                var c = 0;

                var traceFixo = {
                    x: [],
                    y: [],
                    type: 'scatter',
                    name: sensor.d + ' [' + grandeza.n + '] (Intervalo de ' + frequenciaLeitura + ' mins)'
                };
                /** FIM DAS VARIÁVEIS DE TESTE */

                grandeza.l.forEach(function (leitura) {
                    // console.log(leitura);
                    //grafico do valor
                    c = c + 1;
                    if (c % frequenciaLeitura == 0) {
                        traceFixo.y.push(leitura.v);
                        traceFixo.x.push(new Date(leitura.c * 1000));
                    }
                    trace.y.push(leitura.v);
                    trace.x.push(new Date(leitura.c * 1000));
                }, this);
                linhas.push(trace);

                var traceMV = {
                    x: [],
                    y: [],
                    type: 'scatter',
                    name: sensor.d + ' [' + grandeza.n + '] (Intervalo variável)'
                };
                var traceFR = {
                    x: [],
                    y: [],
                    type: 'scatter',
                    name: 'intervalo de leitura',
                    width: []
                };
                var total = grandeza.l.length;
                var leiturasFeitas = 0;
                for (var i = 0; i < grandeza.l.length;) {
                    var leitura = grandeza.l[i];
                    frequenciaLeitura = frequenciaLeitura + seresta.applyRules(leitura, frequenciaLeitura);
                    if (frequenciaLeitura > freqMax) frequenciaLeitura = freqMax;
                    if (frequenciaLeitura < freqMin) frequenciaLeitura = freqMin;
                    // console.log(frequenciaLeitura);
                    //gráfico da média móvel
                    traceMV.y.push(leitura.v);
                    traceMV.x.push(new Date(leitura.c * 1000));
                    //plota o intervalo de leitura
                    traceFR.y.push(frequenciaLeitura);
                    traceFR.x.push(new Date(leitura.c * 1000));
                    traceFR.width.push(3000);
                    i = i + Math.round(frequenciaLeitura);
                    leiturasFeitas = leiturasFeitas + 1;
                }
                linhas.push(traceMV);
                linhas.push(traceFR);
                linhas.push(traceFixo);
                console.log('----------------------------------------');
                console.log('Total do sensor ' + sensor.d + ' [' + grandeza.n + ']: ' + total);
                console.log('Leituras feitas no método fixo: ' + traceFixo.y.length);
                console.log('Leituras feitas no método variável: ' + leiturasFeitas);
            }, this);
        }, this);
        dialog.modal('hide');
        Plotly.newPlot('grafico', linhas, layout);
    });

}