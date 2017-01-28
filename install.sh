#!/bin/bash

#
# MAIN
#
if [ "$(id -u)" != "0" ]; then
	echo "Este programa precisa ser executado com permissões de super-usuário (root)!"
	exit 1
fi

#para o servico caso estiver rodando
service central stop

#verifica se já existe uma instalação
if [ -d /opt/iot.central ]; then
	#remove os arquivos do app existente
	if [ -d /opt/iot.central/interface/ ]; then
		rm -r /opt/iot.central/interface
	fi
	if [ -d /opt/iot.central/placaBase/ ]; then
		rm -r /opt/iot.central/placaBase
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

#Copia os novos arquivos
echo ".Copiando arquivos"
mkdir /opt/iot.central/placaBase

cp -r placaBase/app /opt/iot.central/placaBase
cp -r interface /opt/iot.central/interface

#altera as permissoes dos arquivos
echo "..Alterando as permissões"
chown root:root -R /opt/iot.central
chmod 777 -R /opt/iot.central/placaBase # 554 dono e grupo le e executa, outros leem
chmod 777 -R /opt/iot.central/interface # 554 dono e grupo le e executa, outros leem
chmod 777 -R /opt/iot.central/banco # 604 dono le e escreve, outros leem
echo "ATENÇÃO! REVER AS PERMISSOES DOS ARQUIVOS QUANDO COLOCAR EM PRODUÇÃO"

#copia arquivo do serviço
echo "...Instalando serviço"
cp servico/central.sh /etc/init.d/central
#altera dono e grupo
chown root:root /etc/init.d/central
#altera as permissoes
chmod 755 /etc/init.d/central
#coloca para inicializar junto ao sistema
update-rc.d central defaults


echo "....Atualizando banco de dados"
cd /opt/iot.central/interface
python3 manage.py makemigrations
python3 manage.py migrate

#Reiniciando serviço
echo ".....Iniciando serviço"
service central start
