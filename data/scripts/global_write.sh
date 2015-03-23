find / ! -type l ! -path "/proc/*" ! -user `whoami` -perm -a+w -ls 2>/dev/null
