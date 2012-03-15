#!/bin/sh

rm $0

python2 "aagavin_script2.py"

echo "

------------------
(program exited with code: $?)" 		


echo "Press return to continue"
#to be more compatible with shells like dash
dummy_var=""
read dummy_var
