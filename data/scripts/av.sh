for av in 'rkhunter' 'chkrootkit' 'clamav' 'tripwire' 'snort' 'suricata' 'selinux' 'apparmour' 'samhain' 'ossec-control' 'bro'
do 	for file in `whereis $av | cut -d' ' -f2`
    do 	name="`echo $av|sed -r -e 's/[_\-].*//'`"
        if [ -e "$file" ]
        then echo "[!] $name"
        else echo "[-] $name"
        fi
    done
done
