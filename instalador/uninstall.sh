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
supervisorctl stop centralWeb
supervisorctl stop centralMQTT
supervisorctl stop centralPlacaBase

killall gunicorn

#verifica se existe uma instalação
if [ -d /opt/iot.central ]; then
	#remove os arquivos do app existente
	if [ -d /opt/iot.central/central/ ]; then
		rm -rf /opt/iot.central/central
	fi
fi

#remove servicos no supervisord
rm /etc/supervisor/conf.d/centralWeb.conf
rm /etc/supervisor/conf.d/centralMQTT.conf
rm /etc/supervisor/conf.d/centralPlacaBase.conf
supervisorctl reload

rm -rf /var/www/static

rm /etc/nginx/sites-enabled/central_nginx.conf
ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/
systemctl restart nginx

echo "...Encerrado"
