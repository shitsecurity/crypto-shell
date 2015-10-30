#!/bin/bash

echo 'demo'
for i in $(ls "`pwd`")
do if [ -d "$i" ]
        then printf "[d] "
        else printf "[f] "
    fi
    echo $i
done
