#!/bin/bash

# @autor: xlamac00@stud.fit.vutbr.cz

TASK=../csv.py
INTERPRET="python3"
SUFFIXIN=".csv"
SUFFIXOUT=".xml"
CONT=0
passed=0
failed=0
wsa=0

if [ -t 1 ]; then
    c_red=`tput setaf 1`
    c_green=`tput setaf 2`
    c_normal=`tput sgr0`
fi

function testcsv() {  
 if [ $CONT -ne 0 ]; then
   if [ $CONT -eq $cnt_cont ]; then
     CONT=0;
   else
     cnt_cont=$[$cnt_cont+1]
     return
   fi
 fi
 
 if [ $2 -ne 0 ]; then
   touch ./tests/empty
   FILE="./tests/empty"
 elif ! [ -f ./tests/$1$SUFFIXOUT ]; then
   echo "${c_red}Mising test out: ./tests/$1$SUFFIXOUT $c_normal"
   return
 else
   FILE="./tests/$1$SUFFIXOUT"
 fi
 if ! [ -f ./tests/$1$SUFFIXIN ]; then
   echo "${c_red}Mising test input: ./tests/$1$SUFFIXIN $c_normal"
   return
 fi
 
 $INTERPRET $TASK --input=./tests/$1$SUFFIXIN --output=./tests/$1$SUFFIXOUT.tmp $3 2>/dev/null
 rcode=$?
 cnt=$[$cnt+1]
 fail=0;

   # kontrola navratoveho kodu
 if [ $2 -ne 0 ]; then
   if [ $rcode -eq $2 ]; then
    printf " - RETURN: ${c_green}pass$c_normal"
    if [ -f ./tests/$1_ERROR$SUFFIXOUT ]; then
      rm ./tests/$1_ERROR$SUFFIXOUT
    fi
   else
    printf " - RETURN: ${c_red}FAIL$c_normal"
    fail=$[$fail+1];
    $INTERPRET $TASK --input=./tests/$1$SUFFIXIN --output=./tests/$1_ERROR$SUFFIXOUT $3
   fi
 fi

   # kontrola vystupniho souboru
 if [ $2 -eq 0 ]; then
  if diff -q ./tests/$1$SUFFIXOUT.tmp $FILE > /dev/null && [ $rcode -eq $2 ]; then
    printf " + OUTPUT: ${c_green}pass$c_normal"
    if [ -f ./tests/$1_ERROR$SUFFIXOUT ]; then
      rm ./tests/$1_ERROR$SUFFIXOUT
    fi
   else
    printf " + OUTPUT: ${c_red}FAIL$c_normal"
    fail=$[$fail+2];
    $INTERPRET $TASK --input=./tests/$1$SUFFIXIN --output=./tests/$1_ERROR$SUFFIXOUT $3
   fi
 fi
 printf "\t\t$1 $3\n"

 if [ $fail -ne 0 ]; then
  failed=$[$failed+1]
 else
  passed=$[$passed+1]
 fi

 if [[ $fail == 1 || $fail == 3 ]]; then
  echo "  expected: $2; returned: ${rcode}"
 fi

 cnt_cont=$[$cnt_cont+1]
}

#######################################################################
###########################   T E S T Y   #############################
#######################################################################

# FILENAME EXPECTED_RETURN PARAMETERS
testcsv "fit1" 0 ""
testcsv "fit2" 30 "-l=\"ra-dek\""
testcsv "fit3" 0 "-l=radek -r=root -i -n"
testcsv "fit4" 32 "-s=;"
testcsv "fit5" 0 "-s=; -e "
testcsv "fit6" 0 "--start=2 -h -i -l=data"
testcsv "fit7" 0 ""
testcsv "fit8" 0 ""
testcsv "fit9" 0 "-h -r=róót"
testcsv "fit10" 0 "-h"
testcsv "fit11" 0 "-l=line -i"
testcsv "fit12" 31 "-h"
testcsv "fit13" 0 "--start=5 -i -s=TAB -l=row"
testcsv "fit14" 0 "-s=TAB -h"
testcsv "fit15" 32 "-r=root"
testcsv "fit16" 0 "--all-columns -e -r=root"
testcsv "fit17" 30 "--error-recovery -r=\x20root"
testcsv "fit18" 0 "-e -h=jk --all-columns --missing-field=chybí -c=Kontakt"
#~ 
testcsv "return1" 0 ""
testcsv "return2" 32 ""
testcsv "return1" 30 "-r=\&tralala"
testcsv "return1" 30 "-c=tral&l&"
testcsv "return1" 30 "-l=<row>"
testcsv "return1" 1 "--help"
testcsv "return1" 1 "-l"
testcsv "return1" 1 "-i"
testcsv "return1" 1 "-i --start=42"
testcsv "return1" 1 "-l=row --start=42"
testcsv "return1" 1 "--start=42"
testcsv "return1" 1 "-l=hello -i --start=-42"
testcsv "return1" 1 "-l=hello -i --start=0.5"
testcsv "return1" 1 "-l=hello -i --start=1xtr0ll"
testcsv "return1" 1 "--missing-field=5"
testcsv "return1" 1 "--all-columns"
testcsv "return1" 2 "--input=lol"
#~ testcsv "return1" 3 "--output=tests/norights" #takovyh soubor si kdyztak taky vytvorte :)
testcsv "return3" 31 "-h=0"
testcsv "return3" 0 "-h=x"

testcsv "fituska1" 0 ""

testcsv "internet1" 0 "-r=csv-set -l=csv-record -h"
testcsv "internet2" 0 "-r=company -l=record -i -h --start=1001"
testcsv "internet3" 0 "-r=Inventory -l=Line -n -h -s=-"
testcsv "internet4" 0 "-r=root -n -c=elem -h"
testcsv "internet5" 0 "-r=char -l=name -h -c=film -e --all-columns"

testcsv "bednarik01" 0 "-r=root"
testcsv "bednarik02" 0 "-r=root -n"
testcsv "bednarik03" 0 "-r=root -h"
testcsv "bednarik04" 0 "-r=root -s=,"
testcsv "bednarik05" 0 "-r=root -s=;"
testcsv "bednarik06" 0 "-r=root -l=radek"
testcsv "bednarik07" 0 "-r=root -l=řádek"
testcsv "bednarik08" 30 "-r=root -l=:_.-RaDek123"
testcsv "bednarik09" 0 "-r=root -l=row -i"
testcsv "bednarik10" 0 "-r=root -l=row -i --start=8"
testcsv "bednarik11" 0 "-r=root -l=row -i --start=0"
testcsv "bednarik12" 0 "-r=root -e"
testcsv "bednarik13" 0 "-r=root --error-recovery"
testcsv "bednarik14" 0 "-r=root -e -h"
testcsv "bednarik15" 0 "-r=root -e -h"
testcsv "bednarik16" 0 "-r=root -e --missing-field=chybějící_údaj"
testcsv "bednarik17" 0 "-r=root -e --missing-field=a<b&&c>d"
testcsv "bednarik18" 0 "-r=root -e -h --missing-field=žluťoučký_koník"
testcsv "bednarik19" 0 "-r=root -e --all-columns"
testcsv "bednarik20" 0 "-r=root -e -h --all-columns"
testcsv "bednarik21" 0 "-r=root -e --all-columns --missing-field=trol"
testcsv "bednarik22" 0 "-r=root -e -h --all-columns --missing-field=t"
testcsv "bednarik23" 0 "-r=root -e -h --all-columns --missing-field=vzoreček:ž<ý -l=čočka -i --start=15"
testcsv "bednarik24" 0 "-r=root -s=~ -h"
testcsv "bednarik25" 0 "-r=root -s=TAB -h"
testcsv "bednarik26" 0 "-r=root -h"
testcsv "bednarik27" 0 "-r=root"
testcsv "bednarik28" 0 "-r=root -l=ra-dek"
testcsv "bednarik29" 0 "-r=root -l=radek -i -n"
testcsv "bednarik30" 0 "-r=root -s=; -e"
testcsv "bednarik31" 0 "-r=root --start=2 -h -i -l=data"
testcsv "bednarik32" 0 "-r=root"
testcsv "bednarik33" 0 "-r=root"
testcsv "bednarik34" 0 "-r=róót  -h"
testcsv "bednarik35" 0 "-r=root -h"
testcsv "bednarik36" 0 "-r=root -l=line -i"
testcsv "bednarik37" 0 "-r=root --start=5 -i -s=TAB -l=row"
testcsv "bednarik38" 0 "-r=root -s=TAB -h"
testcsv "bednarik39" 0 "-r=root --all-columns -e"

if [ $passed -eq $cnt ]; then
  echo "CSV result $passed / $cnt"
else
  echo "CSV result ${c_red}$passed ${c_normal} / $cnt"
fi

rm ./tests/*.xml.tmp
