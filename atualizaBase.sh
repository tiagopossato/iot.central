#!/bin/bash
echo "....Atualizando banco de dados"

if [ -z "$1" ]; then
	cd interface
else
	cd $1/interface
fi

# muda nome do arquivo para evitar conflitos
mv central/admin.py central/2admin.py
mv interface/urls.py interface/2urls.py
# renomeia um arquivo vazio para evitar que inicie a aplicação
mv interface/_urls.py interface/urls.py

python3 manage.py makemigrations
python3 manage.py migrate

echo -n "Criar Super Usuario? 1->s , 2->n  "
read resp
if [ $resp -eq 1 ]; then
	python3 manage.py createsuperuser
fi

echo -n "Popular o banco? 1->s , 2->n  "
read resp
if [ $resp -eq 1 ]; then
	python3 central/placaBase/popularBanco.py
fi

echo "update central_entradadigital set estado=0;" > /tmp/tmp.sql
sqlite3 /opt/estufa-central/banco/db.sqlite3 < /tmp/tmp.sql
rm /tmp/tmp.sql

mv central/2admin.py central/admin.py
mv interface/urls.py interface/_urls.py
mv interface/2urls.py interface/urls.py