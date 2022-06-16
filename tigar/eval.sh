for f in test/*.in.*
do
  echo "Testing..." $f
  time ./$1 < $f > out
  diff -Z out ${f/in/out}
done
