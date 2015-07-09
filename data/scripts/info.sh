header() { printf "    [X]%*s\n" $((76 - ${#1})) ''|tr ' ' '-'|sed -e "s/X/$1/"; }
lb() { echo ''; }

header 'Host'
uname -a

lb
header 'Shell'
echo $$DOC_ROOT$$SHELL_FILE

lb
header 'Priv'
id

lb
header 'Uptime'
uptime|sed -e 's/ //'

lb
header 'Memory'
free -m

lb
header 'Disk'
df -H

lb
header 'Mount'
mount

lb
header 'Dir'
ls -ltr

lb
header 'Processes'
for user in `who|cut -d' ' -f1`
	do ps -u "$user" -o user,args,pid,ppid
done

lb
header 'Networks'
`whereis ifconfig|awk '{print $2}'` -a|grep -E '^(\w|\s+inet|$)'|head -n -1

lb
header 'Routing'
`whereis route|awk '{print $2}'` -n

lb
header 'ARP Cache'
`whereis arp|awk '{print $2}'` -n

lb
header 'TCP Connections'
netstat -antp 2>/dev/null

lb
header 'Logged In'
w|tail -n +2

lb
header 'Last Login'
lastlog|grep -vE 'Never'

echo ''
header 'Last Update'
if [ -d /var/cache/apt/ ]
then echo 'apt:' `stat -c %y /var/cache/apt/`
elif [ -d /var/cache/dnf/ ]
then echo 'dnf:' `stat -c %y /var/cache/dnf/`
elif [ -d /var/cache/yum/ ]
then echo 'yum:' `stat -c %y /var/cache/yum/`
fi

lb
header 'Firewall'
`whereis iptables|awk '{print $2}'` -L -t nat
