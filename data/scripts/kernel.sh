echo "[*] kernel: `uname -a`"

recovered=false
unknown='unknown'

if [ -d /proc ]
then echo '[+] /proc enabled'
    if [ ${recovered} = false ]
    then mmap_min_addr=`cat /proc/sys/vm/mmap_min_addr`
        modprobe=`cat /proc/sys/kernel/modprobe`
        kptr=`cat /proc/sys/kernel/kptr_restrict`
        mod_disabled=`cat /proc/sys/kernel/modules_disabled`
        smep=`grep smep /proc/cpuinfo`
        recovered=true
    fi
else echo '[-] /proc disabled'
fi

sysctl=`whereis sysctl|awk '{print $2}'`
if [ -z "${sysctl}" ]
then echo '[-] sysctl not found'
else echo "[+] sysctl: ${sysctl}"
    if [ ${recovered} = false ]
    then mmap_min_addr=`${sysctl} vm.mmap_min_addr|awk '{print $3}'`
        modprobe=`${sysctl} kernel.modprobe|awk '{print $3}'`
        kptr=`${sysctl} kernel.kptr_restrict|awk '{print $3}'`
        mod_disabled=`${sysctl} kernel.modules_disabled|awk '{print $3}'`
        smep=${unknown}
        recovered=true
    fi
fi

if [ $recovered = true ]
then echo "[*] modprobe: ${modprobe}"

    if [ $kptr -eq 0 ]
        then echo '[+] /proc/kallsyms enabled'
        else echo '[-] kallsyms disabled'
    fi

    if [ $mmap_min_addr -lt 65536 ]
        then echo "[+] mmap_min_addr ${mmap_min_addr}"
        else echo "[-] mmap_min_addr ${mmap_min_addr}"
    fi

    if [ $mod_disabled -eq 0 ]
        then echo '[+] lkm enabled'
        else echo '[-] lkm disabled'
    fi

    if [ -z "$smep" ]
        then echo '[+] smep disabled'
    elif [ "$smep" = ${unknown} ]
        then  echo '[!] smep status unknown'
    else echo '[-] smep enabled'
    fi
fi

for f in /boot/System.map-*
do [ -e "$f" ] && echo "[+] system map found" || echo "[-] system map not found"
    break
done
ls -l /boot/System.map-*|sed -r -e 's/\s+/ /g'|cut -d' ' -f1,3,4,6-
