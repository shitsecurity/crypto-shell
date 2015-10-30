for x in `cat /etc/passwd | cut -d: -f1,3,6`
do  name=`echo $x | awk -F: '{print $1}'`
    uid=`echo "$x" | awk -F: '{print $2}'`
    home=`echo $x | awk -F: '{print $3}'`
    echo "$name uid=$uid home=$home"
    find -L $home -perm -a+r -type f -ls 2>/dev/null
done
