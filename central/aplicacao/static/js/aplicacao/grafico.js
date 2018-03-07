var init = function(){
    $('#selectAmbiente').unbind("change");
    $('#selectAmbiente').change(getMetadata);
    moment.locale('pt-br'); 
};

var metadata = new Map();
var dados = {
    'ambiente':{
        'nome':'',
        'id':''
    },
    'metadata':metadata
};

var getMetadata = function(){
    dados['ambiente']['id'] = $("#selectAmbiente option:selected")[0].value;
    dados['ambiente']['nome'] = $("#selectAmbiente option:selected")[0].text;

    if(dados['ambiente']['id']==-1){
        $('#selectGrandeza').addClass('hide');
        $('#selectSensor').addClass('hide');
        $('#selectDateRange').addClass('hide');
        $('#btnDesenharGrafico').addClass('hide');
        return;
    } 

    var dialog = dialogoBuscando();
    
    $.get(window.location.origin + '/app/metadata', { id: dados['ambiente']['id'] }, function (itens) {
        $('#selectGrandeza').addClass('hide');
        $('#selectSensor').addClass('hide');
        $('#btnDesenharGrafico').addClass('hide');
        $('#selectGrandeza')
        .find('option')
        .remove()
        .end()
        .append('<option value="-1">Selecione uma grandeza</option>');
        $.each(itens, function (i, item) {
            metadata.set(item.codigo, item);
            $('#selectGrandeza').append($('<option>', {
                value: item.codigo,
                text : item.nome 
            }));
        });
        $('#selectGrandeza').removeClass('hide');
        $('#selectGrandeza').unbind("change");
        $('#selectGrandeza').change(fillSelectSensor);
        dialog.modal('hide');
    }).fail(function (err) {
        console.log(err);
        dialog.modal('hide');
        bootbox.alert({
            title: "Erro",
            message: err.responseJSON.erro
        });
    });
}

var fillSelectSensor = function(){
    let grandeza = parseInt($("#selectGrandeza option:selected")[0].value);
    if(grandeza==-1){
        $('#selectSensor').addClass('hide');
        $('#selectDateRange').addClass('hide');
        $('#btnDesenharGrafico').addClass('hide');
        return;
    } 
    
    $('#selectSensor')
    .find('option')
    .remove()
    .end()
    .append('<option value="-1">Selecione um sensor</option>');
    $.each(dados['metadata'].get(grandeza)['sensores'], function (i, item) {
        $('#selectSensor').append($('<option>', {
            value: i,
            text : item.descricao 
        }));
    });
     $('#selectSensor').removeClass('hide');
     $('#selectDateRange').addClass('hide');
     $('#btnDesenharGrafico').addClass('hide');
     $('#selectSensor').unbind("change");
     $('#selectSensor').change(showSelectDateRange);
}

var showSelectDateRange = function(){
    let grandeza = parseInt($("#selectGrandeza option:selected")[0].value);
    let indice = $("#selectSensor option:selected")[0].value;
    if(indice==-1){
        $('#selectDateRange').addClass('hide');
        $('#btnDesenharGrafico').addClass('hide');
        return;
    }
    let sensor = dados['metadata'].get(grandeza)['sensores'][indice];
    let minDate = moment(sensor['minDate']).format('DD/MM/YYYY HH:mm');
    let maxDate = moment(sensor['maxDate']).format('DD/MM/YYYY HH:mm');
    let startDate =  moment(sensor['maxDate']).subtract(1, 'days').format('DD/MM/YYYY HH:mm');
    let endDate = maxDate;
    $('#btnDesenharGrafico').unbind("click");
    $('#btnDesenharGrafico').click(function(){
        getLeituras(moment(sensor['maxDate']).subtract(1, 'days').format('YYYY-MM-DD HH:MM'), 
                    moment(sensor['maxDate']).format('YYYY-MM-DD HH:MM'));
    });
    try{
        $('#selectDateRange').data('daterangepicker').remove()
    }catch(e){
        console.log();
    }

  $('#selectDateRange').daterangepicker({
    "showDropdowns": true,
    "timePicker": true,
    "timePicker24Hour": true,
    "locale": {
      "format": "DD/MM/YYYY HH:mm",
      "separator": " - ",
      "applyLabel": "Aplicar",
      "cancelLabel": "Cancelar",
      "fromLabel": "De",
      "toLabel": "Até",
      "customRangeLabel": "Personalizado",
      "weekLabel": "S",
      "daysOfWeek": [
        "Dom",
        "2ª",
        "3ª",
        "4ª",
        "5ª",
        "6ª",
        "Sab"
      ],
      "monthNames": [
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro"
      ],
      "firstDay": 1
    },
    "linkedCalendars": false,
    "showCustomRangeLabel": false,
    "alwaysShowCalendars": true,
    "minDate": minDate,
    "maxDate": maxDate,
    "startDate": startDate,
    "endDate": endDate,
    "opens": "center"
  }, function(start, end, label){
      $('#btnDesenharGrafico').unbind("click");
      $('#btnDesenharGrafico').click(function(){
            getLeituras(moment(start).format('YYYY-MM-DD HH:MM'), moment(end).format('YYYY-MM-DD HH:MM'));
      });
  });
  $('#selectDateRange').removeClass('hide');
  $('#btnDesenharGrafico').removeClass('hide');
}


var getLeituras = function (start, end) {
 
    let grandeza = parseInt($("#selectGrandeza option:selected")[0].value);
    let sensor = dados['metadata'].get(grandeza)['sensores'][$("#selectSensor option:selected")[0].value]['uid'];
    let minDate = start;
    let maxDate = end;
    var dialog = dialogoBuscando();
    $.get(window.location.origin + "/app/grafico",{
        'ambiente': dados['ambiente']['id'],
        'grandeza': grandeza,
        'sensor': sensor,
        'minDate': minDate,
        'maxDate': maxDate
        }, function (dados, status) {
            var layout = {
            legend: {
                orientation: 'h',
                yanchor: 'top',
                xanchor: 'left'
            },
                showlegend: true
            };
            var trace = {
                x: dados.leituras.createdAt,
                y: dados.leituras.valores,
                type: 'scatter',
                name: dados.sensor + ' (' + dados.grandeza + ')'
            }
            dialog.modal('hide');
            Plotly.newPlot('grafico', [trace], layout);
    });
};

var dialogoBuscando = function(){
    return bootbox.dialog({
        message: '<p class="text-center"><i class="fa fa-spin fa-spinner"></i></p><p class="text-center">Buscando dados...</p>',
        closeButton: false,
        size: 'small'
    });
}