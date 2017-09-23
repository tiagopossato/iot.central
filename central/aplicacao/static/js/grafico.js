var initGrafico = function () {
    var myChart = echarts.init(document.getElementById('grafico'));
    // use configuration item and data specified to show chart
    var option = {
        title: {
            text: 'Ultimas 12 horas'
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: []
        },
        // toolbox: {
        //     show: true,
        //     feature: {
        //         dataZoom: {
        //             yAxisIndex: 'none',
        //             name: 'testes'
        //         },
        //         dataView: { readOnly: false },
        //         magicType: { type: ['line', 'bar'] },
        //         restore: {},
        //         saveAsImage: {}
        //     }
        // },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: []
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                formatter: '{value} °C'
            }
        },
        series: []
    };

    myChart.showLoading();
    $.get(location.protocol + "//" + location.host + "/app/leituras", function (data, status) {
        console.log(data);
        data.forEach(function (sensor) {
            // console.log(sensor)
            sensor.g.forEach(function (grandeza) {
                linha = {
                    name: sensor.d,
                    type: 'line',
                    data: [],
                    markPoint: {
                        data: [
                            { type: 'max', name: 'Max' },
                            { type: 'min', name: 'Max' }
                        ]
                    },
                    markLine: {
                        data: [
                            { type: 'average', name: 'Média' }
                        ]
                    }
                }
                grandeza.l.forEach(function(leitura){
                    linha.data.push(leitura.v);
                },this);
                
                // console.log(linha)
                option.legend.data.push(sensor.d+'[' + grandeza.n + ']')
                option.series.push(linha);
            }, this);
        }, this);
        console.log(option);
        myChart.setOption(option);
        myChart.hideLoading();
    });

};