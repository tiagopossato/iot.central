#!/bin/bash

#
# MAIN
#
if [ "$(id -u)" != "0" ]; then
	echo "Este programa precisa ser executado com permissões de super-usuário (root)!"
	exit 1
fi

#para o servico caso estiver rodando
echo ".Parando o serviço"
service central stop

#verifica se existe uma instalação
if [ -d /opt/iot.central ]; then
	#remove os arquivos do app existente
	if [ -d /opt/iot.central/app/ ]; then
		rm -rf /opt/iot.central/app
	fi
fi

echo "..Desinstalando serviço"
update-rc.d -f central remove
#remove arquivo
rm /etc/init.d/central

echo "...Encerrado"
