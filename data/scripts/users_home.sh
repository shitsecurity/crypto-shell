for x in `cat /etc/passwd | cut -d: -f1,3,6`
do  name=`echo $x | awk -F: '{print $1}'`
	uid=`echo "$x" | awk -F: '{print $2}'`
	home=`echo $x | awk -F: '{print $3}'`
	if [ "$uid" -ge 500 ]
	then echo "$name uid=$uid home=$home"
		ls -lah $home --full-time
	fi
done
