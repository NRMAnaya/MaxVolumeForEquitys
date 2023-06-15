#!/bin/bash
SCRIPT_NAME=$(basename -- "$0")
TIME_NOW=$(date)
FULL_PATH=$(realpath $0)
echo "__________________________________________________________________________________________________________________________"
echo "$TIME_NOW"
echo "Running: $SCRIPT_NAME"
echo "Location: $FULL_PATH"
echo "__________________________________________________________________________________________________________________________"

#DATE=$(date +%Y.%m.%d)
#DATE=2023.05.29
#DATE=$1
#echo "esta es la fecha que consultamos $DATE"
HOME_FOLDER=$(eval echo ~$USER) ###/home/ops

echo "N03"

diasRebalanceo="$HOME_FOLDER/ReportesOperaciones/HechosBIVA/RebalanceoDias.txt"
ISINemisorasRebalanceo="$HOME_FOLDER/ReportesOperaciones/HechosBIVA/RebalanceoISINemisoras.txt"


numero=1
dia=1
tiempoVolumen=120 ###esta variable son los segundos, por ejemplo 120 segundos reunira el volumen de 2 minutos, 300 segundos serian 5 mimnutos etc.
inicioDia=27000 ##son las 7:30
finDia=50400 ###son las 14:00:00
diaPorSegundos="$HOME_FOLDER/ReportesOperaciones/HechosBIVA/horasCada"$tiempoVolumen"seg.csv"

while [ "$inicioDia" -le "$finDia" ]; do
        echo "$inicioDia" >> $diaPorSegundos
        inicioDia=$(($inicioDia+$tiempoVolumen));
done

sed -i '1i Hora Final' $diaPorSegundos

################################
###################recorremos el archivo que tiene los ISIN, despues de eso y por cada isin saca un arhcvio por cada dia en el formato ISIN+NUMERO DE DIA 
################################
while IFS= read -r isin;
     do echo "este es el isin: $isin"
          while IFS= read -r date;
                  do
                      echo "empezamos busquea en delta de la fecha: $date del $isin es el  archvio # $dia y elvolumen tiene tiempo de volumende $tiempoVolumen"
		       /usr/bin/java -jar $HOME_FOLDER/kdbQueries/kdbQueriesAndFunctions.jar '{[fecha;instrumento]select from  bivaTrades where date=fecha, ISIN in instrumento, not cxl, not board=`$"OPEL-B", not TradeSourceId in `IP}[('$date');(`$"'$isin'")]' $HOME_FOLDER/kdbQueries/kdb.history.opsapp.properties 2 >> hechosemisora$isin$dia.txt; ##segun el isin bucamos los trades que hizo en ese día
		       echo "Creamos el archvio de volumen con tiempo del $isin el archvio # $dia"
                       /usr/bin/python3 $HOME_FOLDER/ReportesOperaciones/HechosBIVA/RebalanceoImporte.py $isin $dia $date $tiempoVolumen; #ejecutamos el python que los convierte en csv cada 10 minutos pasnadole 
		       echo "empezamos con el join de los archvios y le mandamos estas variables: $dia $isin $date"
                       /usr/bin/python3 $HOME_FOLDER/ReportesOperaciones/HechosBIVA/RebalanceoJoin.py $dia $isin $date;
                       dia=$(($dia+$numero));
          done < $diasRebalanceo
	  dia=1
done < $ISINemisorasRebalanceo


