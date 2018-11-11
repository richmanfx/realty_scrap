#!/bin/sh

# Запускать этот файл чере точку: ". ./make_virtual_env.sh"

VIRTUAL_ENV_DIR='/home/zoer/PycharmProjects/realty_scrap'
VIRTUAL_ENV_NAME='venv'

echo ""
echo " ===> Создание виртуального окружения:"
virtualenv -p python3 ${VIRTUAL_ENV_DIR}/${VIRTUAL_ENV_NAME}


echo ""
echo " ===> Активация виртуального окружения:"
. ${VIRTUAL_ENV_DIR}/${VIRTUAL_ENV_NAME}/bin/activate


echo ""
echo " ===> Инсталляция пакетов из requirements.txt в виртуальном пространстве:"
pwd
pip3 install -r ${VIRTUAL_ENV_DIR}/${VIRTUAL_ENV_NAME}/requirements.txt
