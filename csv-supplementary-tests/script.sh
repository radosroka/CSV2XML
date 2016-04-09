#~/bin/bash

#set -x


cp ../csv2xml.py ./csv.py
cp ~/jexamxml.jar ./
./_stud_tests.sh

for  i in `seq 1 18` ;
do
if [ $i -lt 10 ]; then
	java -jar ./jexamxml.jar test0$i.xml ref-out/test0$i.xml
else 
	java -jar ./jexamxml.jar test$i.xml ref-out/test$i.xml
fi
done

