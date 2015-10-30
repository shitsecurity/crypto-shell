for x in `cat /etc/passwd | cut -d: -f1,3,4,6,7`
do  name=`echo $x | awk -F: '{print $1}'`
    uid=`echo "$x" | awk -F: '{print $2}'`
    gid=`echo $x | awk -F: '{print $3}'`
    home=`echo $x | awk -F: '{print $4}'`
    shell=`echo $x | awk -F: '{print $5}'`
    echo "$name uid=$uid gid=$gid home=$home shell=$shell"
done
