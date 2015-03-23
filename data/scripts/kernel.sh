if [ -d /proc ]
then echo '[+] /proc exists'
	proc=true
else echo '[-] /proc disabled'
	proc=false
fi

skip=false
sysctl=`whereis sysctl|awk '{print $2}'`
if [ -z $sysctl ]
then echo '[!] sysctl not found'
	if [ $proc = true ]
	then echo '[*] recovering via /proc'
		mmap_min_addr=`cat /proc/sys/vm/mmap_min_addr`
		modprobe=`cat /proc/sys/kernel/modprobe`
		kptr=`cat /proc/sys/kernel/kptr_restrict`
		mod_disabled=`cat /proc/sys/kernel/modules_disabled`
	else 'echo [-] access denied'
		skip=true
	fi
else echo "[+] sysctl: $sysctl" 
	mmap_min_addr=`${sysctl} vm.mmap_min_addr|awk '{print $3}'`
	modprobe=`${sysctl} kernel.modprobe|awk '{print $3}'`
	kptr=`${sysctl} kernel.kptr_restrict|awk '{print $3}'`
	mod_disabled=`${sysctl} kernel.modules_disabled|awk '{print $3}'`
fi

if [ $skip = false ]
then if [ $kptr -eq 0 ]
		then echo '[+] /proc/kallsyms'
		else echo '[-] kallsyms disabled'
	fi

	if [ $mmap_min_addr -lt 65536 ]
		then echo "[+] mmap_min_addr ${mmap_min_addr}"
		else echo "[-] mmap_min_addr ${mmap_min_addr}"
	fi

	echo "[*] modprobe: ${modprobe}"

	if [ $mod_disabled -eq 0 ]
		then echo '[+] lkm enabled'
		else echo '[-] lkm disabled'
	fi
fi

for f in /boot/System.map-*
do [ -e "$f" ] && echo "[+] system map" || echo "[-] system map"
	break
done
ls -l /boot/System.map-*|sed -r -e 's/\s+/ /g'|cut -d' ' -f1,3,4,6-
