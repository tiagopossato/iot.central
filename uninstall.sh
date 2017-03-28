#!/bin/bash

#
# MAIN
#
if [ "$(id -u)" != "0" ]; then
	echo "Este script precisa ser executado com permissões de super-usuário (root)!"
	exit 1
fi

#para o servico caso estiver rodando
echo ".Parando o serviço"
service central stop

#verifica se existe uma instalação
if [ -d /opt/estufa-central ]; then
	#remove os arquivos do app existente
	if [ -d /opt/estufa-central/interface/ ]; then
		rm -rf /opt/estufa-central/interface
	fi
fi

#remove servicos no supervisord
rm /etc/supervisor/conf.d/central.conf
supervisorctl reload

echo "..Desinstalando serviço"
update-rc.d -f central remove
#remove arquivo
rm /etc/init.d/central

echo "...Encerrado"
