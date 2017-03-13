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
if [ -d /opt/iot.central ]; then
	#remove os arquivos do app existente
	# if [ -d /opt/iot.central/placaBase/app/ ]; then
	# 	rm -rf /opt/iot.central/placaBase/app
	# fi
	#remove os arquivos do app existente
	if [ -d /opt/iot.central/interface/ ]; then
		rm -rf /opt/iot.central/interface
	fi
fi

rm /etc/supervisor/conf.d/sincronizaAlarmes.conf
supervisorctl reload

echo "..Desinstalando serviço"
update-rc.d -f central remove
#remove arquivo
rm /etc/init.d/central

echo "...Encerrado"
