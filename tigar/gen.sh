#!/bin/bash

python gen.py

for f in test/*.in.*
do
  ./pavic < $f > ${f/in/out}
done
