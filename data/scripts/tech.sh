gcc -v | tail -n 1 2>/dev/null
g++ -v | tail -n 1 2>/dev/null
clang -v | head -n 1 2>/dev/null
php -v | head -n 1 2>/dev/null
perl -v | grep 'This is perl' | sed -e 's/This is //'
python -V
ruby -v
printf 'node.js '; node -v
