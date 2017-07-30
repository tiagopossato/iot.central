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
    return new Promise(
        function (resolve, reject) {
            $.post('http://' + window.location.host + '/comunicacao/reativar', { username: params.username, password: params.password, servidor: params.servidor, id: params.id }, function (res) {
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

window.onload = function () {
    $('#btn-nova-chave').on('click', function (e) {
        bootbox.confirm({
            title: "Confirmação",
            message: "Gerar nova chave?",
            size: 'small',
            callback: function (result) {
                if (result) {
                    autenticacao().then(function (auth) {
                        $.get('http://' + window.location.host + '/comunicacao/novo-certificado', { username: auth.username, password: auth.password }, function (res) {
                            console.log(res);
                            location.reload();
                        }).fail(function (err) {
                            console.log(err);
                            bootbox.alert({
                                title: "Erro",
                                message: err.responseJSON.erro
                            });
                        });
                    }).catch(function (err) {
                        bootbox.alert({
                            title: "Erro",
                            message: err.responseJSON.erro
                        });
                        console.log(err);
                    });
                }
            }
        });
    });

    $('#btn-inativar').on('click', function (e) {
        bootbox.confirm({
            title: "Confirmação",
            message: "Inativar esta central?",
            size: 'small',
            callback: function (result) {
                if (result) {
                    autenticacao().then(function (auth) {
                        $.get('http://' + window.location.host + '/comunicacao/inativar', { username: auth.username, password: auth.password }, function (res) {
                            location.reload();
                        }).fail(function (err) {
                            bootbox.alert({
                                title: "Erro",
                                message: err.responseJSON.erro
                            });
                            console.log(err);
                        });
                    }).catch(function (err) {
                        console.log(err);
                    });
                }
            }
        });
    });
};

var autenticacao = function () {
    return new Promise(
        function (resolve, reject) {
            bootbox.confirm({
                title: 'Autenticação no servidor',
                size: 'small',
                message: '\
                <form id="form-auth" action="" data-parsley-validate class="form-horizontal form-label-left">\
                    <div class="form-group" >\
                        <label for="username" class="control-label col-md-3 col-sm-3 col-xs-12">Login</label>\
                        <div class="col-md-6 col-sm-6 col-xs-12">\
                            <input id="username" name="username" class="form-control col-md-7 col-xs-12" type="text" placeholder="Usuário"\
                                tabindex="0" autocomplete="off">\
                        </div>\
                    </div>\
                    <div class="form-group">\
                        <label for="password" class="control-label col-md-3 col-sm-3 col-xs-12">Senha</label>\
                        <div class="col-md-6 col-sm-6 col-xs-12">\
                            <input id="password" name="password" class="form-control col-md-7 col-xs-12" type="password" placeholder="Senha"\
                                tabindex="1" autocomplete="off">\
                        </div>\
                    </div>\
                </form>',
                callback: function (result) {
                    if (result == false) {
                        reject("Cancelado");
                    }

                    $('#form-auth').unbind('submit');
                    $('#form-auth').submit(function (event) {
                        event.preventDefault();
                        //serializa o form
                        var unindexed_array = $(this).serializeArray();
                        var _dados = {};
                        $.map(unindexed_array, function (n, i) {
                            _dados[n['name']] = n['value'];
                        });
                        try {
                            var auth = {
                                'username': _dados['username'],
                                'password': _dados['password']
                            }
                            resolve(auth);
                        }
                        catch (e) {
                            reject(e);
                        }

                    });
                    $('#form-auth').submit();
                }
            });
        });
};