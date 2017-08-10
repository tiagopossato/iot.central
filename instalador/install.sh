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

apt install python3 python-pip python3-pip nginx supervisor
pip install virtualenvwrapper

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

read -p "Substituir o banco de dados? [s/N]:" -n 1 -r
echo
case "$REPLY" in 
  s|S )
		cp  ../central/banco/db.sqlite3 /opt/iot.central/banco/
		# Popula o banco
		sqlite3 /opt/iot.central/banco/db.sqlite3 < default.sql
	;;
    * );;
esac

# Altera a variavel de DEBUG para False
sed -i '/DEBUG = True/c\DEBUG = False' /opt/iot.central/central/central/settings.py

echo "..Colentando arquivos estaticos"
python3 /opt/iot.central/central/manage.py collectstatic

# Cria pasta para os certificados
mkdir /opt/iot.central/central/certs

echo "...Alterando permissoes"

# Tudo pertence ao usuario da central
chown central:nogroup /opt/iot.central -R
# Todos podem acessar o primeiro nivel de pastas
chmod 0755 /opt/iot.central

# Somente root e o usuario da central podem acessar a pasta e subpastas
#  da aplicacao e do banco
chmod 0700 /opt/iot.central/central -R
chmod 0700 /opt/iot.central/banco -R

# Os usuarios do grupo www-data também podem escrever na pasta de log
chown central:www-data /opt/iot.central/log -R
# Todos os usuarios podem visualizar os arquivos de log
chmod 0775 /opt/iot.central/log -R
# Somente o usuario www-data pode acessar a pasta de arquivos estaticos
chown www-data:www-data /var/www/static

cp centralWeb.conf /etc/supervisor/conf.d/centralWeb.conf
cp centralMQTT.conf /etc/supervisor/conf.d/centralMQTT.conf
cp centralPlacaBase.conf /etc/supervisor/conf.d/centralPlacaBase.conf

echo "central ALL=(ALL) NOPASSWD: /usr/bin/supervisorctl restart centralMQTT,  /usr/bin/supervisorctl restart centralPlacaBase" > /etc/sudoers.d/central
supervisorctl reload

echo "....Configurando nginx para servir os arquivos estaticos"
cp central_nginx.conf /etc/nginx/sites-available
rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/central_nginx.conf /etc/nginx/sites-enabled/
systemctl restart nginx

