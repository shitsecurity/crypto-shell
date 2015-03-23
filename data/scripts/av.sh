for av in 'rkhunter' 'chkrootkit' 'clamav' 'tripwire'
do 	for file in `whereis $av | cut -d' ' -f2`
	do 	if [ -e "$file" ]
		then echo "[!] $av"
		else echo "[-] $av"
		fi
	done
done
