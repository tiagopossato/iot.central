#!/bin/bash

#
# MAIN
#
if [ "$(id -u)" != "0" ]; then
	echo "Este script precisa ser executado com permissões de super-usuário (root)!"
	exit 1
fi

diretorio=$(pwd)

#para o servico caso estiver rodando
#echo "Parando o serviço"
service central stop

echo "Desinstalando versão instalada"

sh uninstall.sh

#verifica se já existe uma instalação
if [ -d /opt/estufa-central ]; then
	#remove os arquivos do app existente
	if [ -d /opt/estufa-central/interface/ ]; then
		rm -r /opt/estufa-central/interface
	fi
else
	mkdir /opt/estufa-central
fi

#verifica a existencia da pasta do banco de dados
if [ -d /opt/estufa-central/banco ]; then
	echo "A pasta do banco de dados já existe, nada a fazer aqui"
else
	#cria pasta do banco de dados e altera as permissoes
	echo "Criando pasta do banco de dados"
	mkdir /opt/estufa-central/banco
fi

#Copia os novos arquivos
echo ".Copiando arquivos"

cp -r interface /opt/estufa-central/

#
#copia arquivo do serviço
echo "...Instalando serviço"
cp servico/central.sh /etc/init.d/central
#altera dono e grupo
chown root:root /etc/init.d/central
#altera as permissoes
chmod 755 /etc/init.d/central
#coloca para inicializar junto ao sistema
update-rc.d central defaults
#

echo "...instalando servico da central"
cp servico/central.conf /etc/supervisor/conf.d/central.conf


sh $diretorio/atualizaBase.sh $diretorio

#altera as permissoes dos arquivos
echo "..Alterando as permissões"
chown root:root -R /opt/estufa-central
# chmod 777 -R /opt/estufa-central/placaBase # 554 dono e grupo le e executa, outros leem
chmod 777 -R /opt/estufa-central/interface # 554 dono e grupo le e executa, outros leem
chmod 777 -R /opt/estufa-central/banco # 604 dono le e escreve, outros leem
echo "ATENÇÃO! REVER AS PERMISSOES DOS ARQUIVOS QUANDO COLOCAR EM PRODUÇÃO"

#Reiniciando serviço
echo ".....Reiniciando serviço"
service central restart
supervisorctl reload