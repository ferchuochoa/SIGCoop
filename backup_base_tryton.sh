#! /bin/bash
# Copyright © 2011 onwards
# Licencia
# Script de Backup en base de datos Postgres.

if [ $# -ne 2 ]; then
    echo "uso:"
    echo "backup_base_tryton.sh <directorio de backup> <nombre base de datos a backupear>"
    exit 1
fi

# CONFIGURACION
DIA=`date +%Y.%m.%d.%H.%M`
NOMBRE=backup_tryton_ndb.${DIA}.dmp
BACKUP_DIR="$1"
export PGPASSWORD=postgres
NOMBRE_BASE="$2"
# FIN CONFIGURACION

if [ ! -d $BACKUP_DIR ]; then
    mkdir -p $BACKUP_DIR
fi

cd $BACKUP_DIR
touch ${NOMBRE}
chmod 775 ${NOMBRE}

vacuumdb -U postgres -h localhost -d ${NOMBRE_BASE} -f -z
pg_dump -U postgres -h localhost -F p -b -E 'UTF8' -v -f ${NOMBRE} ${NOMBRE_BASE}

retorno=$?

if [ $retorno -ne 0 ]
then
   echo 'Error durante la ejecución del backup. Compruebe: usuario y permisos'
else
   echo 'Backup realizado correctamente. Archivo: ' ${BACKUP_DIR}/${NOMBRE}
fi
#echo ${DIA} '         Reiniciando la base de datos...'
#service postgresql restart
