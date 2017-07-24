/**
 * Função para consultar as centrais inativas no servidor
 * @param {*url, username, password} params 
 */
var getCentraisInativas = function (params) {
    // TODO: Validar os parâmetros recebidos
    return new Promise(
        function (resolve, reject) {
            $.get('http://' + window.location.host + '/comunicacao/centrais-inativas', { username: params.username, password: params.password, servidor: params.servidor }, function (res) {
                try {
                    if (res.erro) {
                        reject(res);
                    }
                    resolve(res);
                }
                catch (err) {
                    reject(err);
                }
            }).fail(function (err) {
                reject(err);
            });
        });
};

/**
 * Solicita os dados da central 'id' ao servidor e configura a central com os dados recebidos
 * @param {*id, url, username, password} params 
 */
var trocaCentral = function (params) {
    // TODO: Validar os parâmetros recebidos
    console.log(params);
    return new Promise(
        function (resolve, reject) {
            $.post('http://' + window.location.host + '/comunicacao/reativar', { username: params.username, password: params.password, servidor: params.servidor, id: params.id}, function (res) {
                try {
                    if (res.erro) {
                        reject(res);
                    }
                    resolve(res);
                }
                catch (err) {
                    reject(err);
                }
            }).fail(function (err) {
                reject(err);
            });
        });
};