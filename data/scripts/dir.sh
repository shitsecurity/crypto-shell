flags="-ALlah --full-time"
echo "/etc/:"
ls ${flags} /etc/ 2>/dev/null
echo "\n/etc/init.d/:"
ls ${flags} /etc/init.d/ 2>/dev/null
echo ""
ls ${flags} /etc/cron.*/ 2>/dev/null
echo "\n/usr/local/etc/:"
ls ${flags} /usr/local/etc/ 2>/dev/null
echo "\n/var/spool/cron/:"
ls ${flags} /var/spool/cron/ 2>/dev/null
echo "\n/var/www/:"
ls ${flags} /var/www/ 2>/dev/null
ls ${flags} /var/www/*/ 2>/dev/null
echo "\n/home/:"
ls ${flags} /home/ 2>/dev/null
echo ""
ls ${flags} /home/*/ 2>/dev/null
echo "\n/lib/:"
ls ${flags} /lib/
echo "\n/lib64/:"
ls ${flags} /lib64/
echo "\n/boot:"
ls ${flags} /boot
echo "\n/:"
ls ${flags} /
