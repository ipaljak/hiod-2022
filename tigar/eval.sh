for f in test/*.in.*
do
  echo "Testing..." $f
  time ./$1 < $f > out
  #diff -Z ${f/.in./.out.} out
done
rm out
