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
	if [ -d /opt/iot.central/app/ ]; then
		rm -r /opt/iot.central/app
	fi
else
	mkdir /opt/iot.central
fi

#verifica a existencia da pasta do banco de dados
if [ -d /opt/iot.central/Banco ]; then
	echo "A pasta do banco de dados já existe, nada a fazer aqui"
else
	#cria pasta do banco de dados e altera as permissoes
	echo "Criando pasta do banco de dados"
	mkdir /opt/iot.central/Banco
fi

#Copia os novos arquivos
echo ".Copiando arquivos"
cp -r app/ /opt/iot.central/app

#altera as permissoes dos arquivos
echo "..Alterando as permissões"
chown root:root -R /opt/iot.central
chmod 777 -R /opt/iot.central/app # 554 dono e grupo le e executa, outros leem
chmod 777 -R /opt/iot.central/Banco # 604 dono le e escreve, outros leem
echo "ATENÇÃO! REVER AS PERMISSOES DOS ARQUIVOS QUANDO COLOCAR EM PRODUÇÃO"

#copia arquivo do serviço
echo "...Instalando serviço"
cp central.sh /etc/init.d/central
#altera dono e grupo
chown root:root /etc/init.d/central
#altera as permissoes
chmod 755 /etc/init.d/central
#coloca para inicializar junto ao sistema
update-rc.d central defaults

#Reiniciando serviço
echo "....Iniciando serviço"
service central start
