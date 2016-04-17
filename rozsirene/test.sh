#! /bin/sh
# Skript je potreba spustit jako ./test.sh < params
# Vystupy skriptu $skript se ulozi do souboru *.out2 a porovnaji s referencnimi
# *.out programem $xmlcmp.

script="csv.py"; 	# Jmeno testovaneho skriptu
res=0;           	# Navratova hodnota testu
xmlcmp="jexamxml.jar";	# SW pro porovnani XML
script="csv.py"		# Jmeno skriptu
spravne=0;

# vyber vstupu
for i in *.in; do
  read line;
  params=`echo $line | sed -r "s/${i%.in}://"`;
  ./$script $params < $i > ${i%in}out2;

  ret=$?;
  if [ $ret != 0 ]; then
    echo "[ERR]: $i ($ret vs 0)";
    res=1;
  else
    # Porovnani s referencnim XML
    java -jar $xmlcmp ${i%in}out ${i%in}out2 delta.xml -D options > /dev/null
    ret=$?;
    if [ $ret != 0 ]; then
      echo "[ERR]: $i ($xmlcmp = $ret)";
      res=1;
    else
      echo "[OK]: $i";
      spravne=$((spravne + 1));
    fi
  fi
done

rm delta.xml 2>/dev/null
echo $spravne;
exit $res;
