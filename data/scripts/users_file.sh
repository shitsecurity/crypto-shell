for x in `cat /etc/passwd | cut -d: -f1,3,6`
do  name=`echo $x | awk -F: '{print $1}'`
	uid=`echo "$x" | awk -F: '{print $2}'`
	home=`echo $x | awk -F: '{print $3}'`
	echo "$name uid=$uid home=$home"
    ls -lah $home -d --full-time
    ls -lah $home/.bash_profile 2>/dev/null
    ls -lah $home/.bashrc 2>/dev/null
    ls -lah $home/.bash_login 2>/dev/null
    ls -lah $home/.profile 2>/dev/null
    ls -lah $home/.bash_logout 2>/dev/null
    ls -lah $home/.bash_history 2>/dev/null
    ls -lah $home/.ssh -d --full-time 2>/dev/null
    ls -lah $home/.ssh/id_rsa 2>/dev/null
    ls -lah $home/.ssh/id_dsa 2>/dev/null
    ls -lah $home/.ssh/id_ecdsa 2>/dev/null
    ls -lah $home/.ssh/known_hosts 2>/dev/null
    ls -lah $home/.ssh/authorized_keys 2>/dev/null
    ls -lah $home/.ssh/authorized_hosts 2>/dev/null
done
