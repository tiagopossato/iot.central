/**
 * Sensor Energy Save Algorithm
 * 
 * Algoritmo para economia de energia em sensores sem fio
 */

/** Calcula média móvel */
//Função que armazena os valores
//Programado desta forma para facilitar 
//a portabilidade para c/c++
//buffer com os valores para o cálculo
var bufferMax = 3;
var bufferQtd = 0;
var bufferData = []; // bufferData[bufferMax]
//Classe que representa um valor
// representada por uma struct em c/c++
class Value {
    constructor() {
        this.v = 0;
        this.t = 0;
    }
};
/**
 * Insere um novo valor no buffer circular
 * para calcular a média móvel
 * @param {*} newValue 
 * @param {*} timestamp 
 */
var valuePush = function (newValue, timestamp) {
    value = new Value();
    value.v = newValue;
    value.t = timestamp;
    if (bufferQtd < bufferMax) {
        bufferData[bufferQtd] = value
        bufferQtd = bufferQtd + 1;
    } else {
        for (var i = 0; i < bufferMax; i++) {
            if (i == bufferMax - 1) {
                bufferData[i] = value;
            } else {
                bufferData[i] = bufferData[i + 1];
            }
        }
    }
    // console.log(bufferData);
};

/**
 * Calcula média dos valores armazenados
 */
var avgCalc = function () {
    var sum = 0;
    for (var i = 0; i < bufferQtd; i++) {
        sum = sum + bufferData[i].v;
    }
    return sum / bufferQtd;
};

/**
 * Calcula a pertinência entre o valor atual e 
 * a média móvel conforme as regras
 * @param {*} value 
 */
var pcMovingAverage = function (value) {
    //verifica se é um número
    if (isNaN(value)) {
        throw "The value must be a number";
    }

    // Limita a valores menores que 1
    if (value > 1) {
        value = 1;
    }
    //calcula valor baixo
    var low = 0;
    if (value < 0.75) {
        low = interpolate(value, 0, 0.75, 1, 0);
    }

    //calcula valor médio
    var medium = 0;
    if (value < 0.125) {
        medium = 0;
    }
    if (value >= 0.125 && value <= 0.875) {
        if (value == 0.5) {
            medium = 1;
        }
        if (value < 0.5) {
            medium = interpolate(value, 0.125, 0.5, 0, 1);
        }
        if (value > 0.5) {
            medium = interpolate(value, 0.5, 0.875, 1, 0);
        }
    }
    if (value > 0.875) {
        medium = 0;
    }

    //calcula valor alto
    var high = 0;
    if (value > 0.25) {
        high = interpolate(value, 0.25, 1, 1, 0);
    }

    return { 'high': high, 'medium': medium, 'low': low };
}

/**
 * Calcula a pertinência da frequencia de leitura dos sensores
 * conforme as regras de pertinência
 * @param {*} value 
 */
var pcReadFrequency = function (value) {
    //verifica se é um número
    if (isNaN(value)) {
        throw "The value must be a number";
    }

    // Limita a valores menores que 1
    if (value > 1) {
        value = 1;
    }
    //calcula valor baixo
    var low = 0;
    if (value < 0.75) {
        low = interpolate(value, 0, 0.75, 1, 0);
    }

    //calcula valor médio
    var medium = 0;
    if (value < 0.125) {
        medium = 0;
    }
    if (value >= 0.125 && value <= 0.875) {
        if (value == 0.5) {
            medium = 1;
        }
        if (value < 0.5) {
            medium = interpolate(value, 0.125, 0.5, 0, 1);
        }
        if (value > 0.5) {
            medium = interpolate(value, 0.5, 0.875, 1, 0);
        }
    }
    if (value > 0.875) {
        medium = 0;
    }

    //calcula valor alto
    var high = 0;
    if (value > 0.25) {
        high = interpolate(value, 0.25, 1, 1, 0);
    }

    return { 'high': high, 'medium': medium, 'low': low };
}

/**
 * Calula interpolação linear
 * 
 * @param {*} input 
 * @param {*} inMin 
 * @param {*} inMax 
 * @param {*} outMin 
 * @param {*} outMax 
 */
var interpolate = function (input, inMin, inMax, outMin, outMax) {
    //verifica se é um número
    if (isNaN(input) || isNaN(inMin) || isNaN(inMax) || isNaN(outMin) || isNaN(outMax)) {
        throw "The value must be a number";
    }
    if (input > inMax || input < inMin) {
        throw "'input' must be between 'inMax' and 'inMin'";
    }
    return (outMax - outMin) * (input - inMin) / (inMax - inMin) + outMin;
};




/**
 * Fuzzifica Taxa de variacao
 * NÃO USADO
 */
var fuzzyRate = function (rate) {
    //verifica se é um número
    if (isNaN(rate)) {
        throw "The value must be a number";
    }
    //verifica se valor está nebuloso
    if (rate < 0 || rate > 1) {
        throw "The value must be between 0 and 1";
    }
    /** Calcula taxa baixa y^2 */
    //inverte valor    
    var rinv = interpolate(rate, 0, 1, 1, 0);
    var rb = rinv * rinv;

    /** Calcula taxa média (-(x^2)+x)*4 */
    var rm = (-(rate * rate) + rate) * 4;

    /** Calcula taxa alta x^2*/
    var ra = rate * rate;
    return { 'high': ra, 'medium': rm, 'low': rb };
};
