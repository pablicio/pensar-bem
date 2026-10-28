#!/bin/bash
destino=/media/pi/BACKUP/leituras
cd $destino
tar -czf leituras-antigas.tar.gz /home/pi/monitor/antigas.csv
rm -f *.csv
