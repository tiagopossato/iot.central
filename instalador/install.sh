#!/bin/bash

#
# MAIN
#
if [ "$(id -u)" != "0" ]; then
	echo "Este script precisa ser executado com permissões de super-usuário (root)!"
	exit 1
fi

diretorio=$(pwd)

#instala as dependencias

apt install python3 python3-pip nginx
pip3 install virtualenvwrapper

linha=("export WORKON_HOME=/opt/.envs")
cat /etc/profile | grep "$linha"
if [ $? -eq 1 ]; then
	echo $linha >> /etc/profile
fi

linha=("source /usr/local/bin/virtualenvwrapper.sh")
cat /etc/profile | grep "$linha"
if [ $? -eq 1 ]; then
	echo $linha >> /etc/profile
fi

source /etc/profile

mkvirtualenv centralvenv --python=python3
workon centralvenv

pip3 install -r requirements.txt

#cria usuario sem grupo e nem login
useradd -g nogroup -M -r -s /usr/sbin/nologin central

echo
echo
echo
echo "Criar usuario para acesso remoto"
echo
echo
echo

#verifica se já existe uma instalação
if [ -d /opt/iot.central ]; then
	#remove os arquivos do app existente
	if [ -d /opt/iot.central/central/ ]; then
		rm -r /opt/iot.central/central
	fi
else
	mkdir /opt/iot.central
fi

#verifica a existencia da pasta do banco de dados
if [ -d /opt/iot.central/banco ]; then
	echo "A pasta do banco de dados já existe, nada a fazer aqui"
else
	#cria pasta do banco de dados e altera as permissoes
	echo "Criando pasta do banco de dados"
	mkdir /opt/iot.central/banco
fi

#verifica a existencia da pasta de log
if [ -d /opt/iot.central/log ]; then
	echo "A pasta de log de dados já existe, nada a fazer aqui"
else
	echo "Criando pasta de log"
	mkdir /opt/iot.central/log
fi


#Copia os novos arquivos
echo ".Copiando arquivos"
cp -r  ../central /opt/iot.central/

# Altera a variavel de DEBUG para False
sed -i '/DEBUG = True/c\DEBUG = False' /opt/iot.central/central/settings.py

echo "..Colentando arquivos estaticos"
python3 /opt/iot.central/central/manage.py collectstatic

echo "...Alterando permissoes"
chown central:www-data /opt/iot.central -R
chmod 0750 /opt/iot.central/central -R

chown central:nogroup /opt/iot.central/banco -R
chmod 0700 /opt/iot.central/banco -R

chown central:nogroup /opt/iot.central/central/certs -R
chmod 0700 /opt/iot.central/central/certs -R

chown central /opt/iot.central/log -R
chmod 0666 /opt/iot.central/log -R

cp centralWeb.conf /etc/supervisor/conf.d/centralWeb.conf
supervisorctl reload

echo "....Configurando nginx para servir os arquivos estaticos"
cp central_nginx.conf /etc/nginx/sites-available
rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/central_nginx.conf /etc/nginx/sites-enabled/
systemctl restart nginx

