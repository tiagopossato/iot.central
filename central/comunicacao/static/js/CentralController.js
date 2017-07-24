/**
 * Função para consultar as centrais inativas no servidor
 * @param {*url, username, password} params 
 */
var getCentraisInativas = function (params) {
    // TODO: Validar os parâmetros recebidos
    
    return new Promise(
        function (resolve, reject) {
            $.get('http://'+window.location.host+'/comunicacao/centrais-inativas', { username: params.username, password: params.password, url:params.url }, function (res) {
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