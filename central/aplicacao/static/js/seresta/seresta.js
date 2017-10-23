/**
 * Sensor Energy Save Algorithm
 * 
 * Algoritmo para economia de energia em sensores sem fio
 */
class Seresta {
    /**
     * 
     * @param {*} freqMin 
     * @param {*} freqMax 
     */
    constructor(freqMin, freqMax) {
        this.freqMin = freqMin;
        this.freqMax = freqMax;
        this.bufferMax = 3;
        this.bufferQtd = 0;
        this.bufferData = [];
    };
    pushValue(newValue, timestamp) {
        let value = {
            v: newValue,
            t: timestamp
        };
        if (this.bufferQtd < this.bufferMax) {
            this.bufferData[this.bufferQtd] = value
            this.bufferQtd = this.bufferQtd + 1;
        } else {
            for (var i = 0; i < this.bufferMax; i++) {
                if (i == this.bufferMax - 1) {
                    this.bufferData[i] = value;
                } else {
                    this.bufferData[i] = this.bufferData[i + 1];
                }
            }
        }
        // console.log(this.bufferData);
    };

    mvAvg() {
        let sum = 0;
        for (let i = 0; i < this.bufferData.length; i++) {
            sum = sum + this.bufferData[i].v;
        }
        return sum / this.bufferQtd;
    };


    /**
     * Calcula a pertinência entre o valor atual e 
     * a média móvel conforme as regras
     * @param {*} value 
     */
    pcMovingAverage(value) {
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
            low = this.interpolate(value, 0, 0.75, 1, 0);
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
                medium = this.interpolate(value, 0.125, 0.5, 0, 1);
            }
            if (value > 0.5) {
                medium = this.interpolate(value, 0.5, 0.875, 1, 0);
            }
        }
        if (value > 0.875) {
            medium = 0;
        }

        //calcula valor alto
        var high = 0;
        if (value > 0.25) {
            high = this.interpolate(value, 0.25, 1, 1, 0);
        }

        return { 'high': high, 'medium': medium, 'low': low };
    }

    /**
     * Calcula a pertinência da frequencia de leitura dos sensores
     * conforme as regras de pertinência
     * 
     * @param {*} value Frequencia atual de leitura dos sensores
     */
    pcReadFrequency(value) {
        //verifica se é um número
        if (isNaN(value)) {
            throw "The value must be a number.";
        }
        if (value > this.freqMax || value < this.freqMin) {
            throw "The value is out of range.";
        }

        // normaliza entrada
        value = this.interpolate(value, this.freqMin, this.freqMax, 0, 1);

        //calcula valor baixo
        var low = 0;
        if (value < 0.75) {
            low = this.interpolate(value, 0, 0.75, 1, 0);
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
                medium = this.interpolate(value, 0.125, 0.5, 0, 1);
            }
            if (value > 0.5) {
                medium = this.interpolate(value, 0.5, 0.875, 1, 0);
            }
        }
        if (value > 0.875) {
            medium = 0;
        }

        //calcula valor alto
        var high = 0;
        if (value > 0.25) {
            high = this.interpolate(value, 0.25, 1, 1, 0);
        }

        return { 'high': high, 'medium': medium, 'low': low };
    };

    r1() {
        if (this.diffMvAvg.high < this.readFrequency.low)
            return this.diffMvAvg.high;
        return this.readFrequency.low;
    };
    r2() {
        if (this.diffMvAvg.medium < this.readFrequency.low)
            return this.diffMvAvg.medium;
        return this.readFrequency.low;
    };
    r3() {
        if (this.diffMvAvg.low < this.readFrequency.low)
            return this.diffMvAvg.low;
        return this.readFrequency.low;
    };

    r4() {
        if (this.diffMvAvg.high < this.readFrequency.medium)
            return this.diffMvAvg.high;
        return this.readFrequency.medium;
    };
    r5() {
        if (this.diffMvAvg.medium < this.readFrequency.medium)
            return this.diffMvAvg.medium;
        return this.readFrequency.medium;
    };
    r6() {
        if (this.diffMvAvg.low < this.readFrequency.medium)
            return this.diffMvAvg.low;
        return this.readFrequency.medium;
    };

    r7() {
        if (this.diffMvAvg.high < this.readFrequency.high)
            return this.diffMvAvg.high;
        return this.readFrequency.high;
    };
    r8() {
        if (this.diffMvAvg.medium < this.readFrequency.high)
            return this.diffMvAvg.medium;
        return this.readFrequency.high;
    };
    r9() {
        if (this.diffMvAvg.low < this.readFrequency.high)
            return this.diffMvAvg.low;
        return this.readFrequency.high;
    };
    /**
     * Recebe o valor atual e efetua os cálculos
     * value.v = leitura
     * value.c = timestamp (createdAt)
     * @param {*} value 
     */
    applyRules(value, frequenciaLeitura) {
        //insere valor para calcular média móvel
        this.pushValue(value.v, value.c);
        //calcula média
        let media = this.mvAvg();
        //calculo da pertinencia da diferença entre o valor atual 
        // e a média móvel
        let diferenca = Math.abs(value.v - media);
        // console.log('pcMovingAverage:');
        this.diffMvAvg = this.pcMovingAverage(diferenca);
        // console.log('pcReadFrequency:');
        this.readFrequency = this.pcReadFrequency(frequenciaLeitura);
        // console.log(readFrequency);

        //tentativa 1
        var increase = this.r1() + this.r2() + this.r4() + this.r8();
        var decrease = this.r3() + this.r5() + this.r5() + this.r7() + this.r9();
        //resultado 1.1
        // var soma = decrease - increase;
        // return soma;
        //resultado 1.2
        if (increase < decrease) return -.25;
        if (increase > decrease) return .5;
        return 0;

        //tentativa 2
        // var soma = this.diffMvAvg.low - this.diffMvAvg.high;

        // return soma;
    };
    
    /**
     * Calula interpolação linear
     * 
     * @param {*} input 
     * @param {*} inMin 
     * @param {*} inMax 
     * @param {*} outMin 
     * @param {*} outMax 
     */
    interpolate(input, inMin, inMax, outMin, outMax) {
        //verifica se é um número
        if (isNaN(input) || isNaN(inMin) || isNaN(inMax) || isNaN(outMin) || isNaN(outMax)) {
            throw "The value must be a number";
        }
        if (input > inMax || input < inMin) {
            throw "'input' must be between 'inMax' and 'inMin'";
        }
        return (outMax - outMin) * (input - inMin) / (inMax - inMin) + outMin;
    };
};