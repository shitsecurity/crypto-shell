$obd = ini_get('open_basedir');
if (trim($obd) != '' ) {
    echo "[!] open_basedir $obd\n";
}

$aui = (ini_get('allow_url_include')==1) ? "on":"off";
echo "[*] allow_url_include: ${aui}\n";

$auo = (ini_get('allow_url_fopen')==1) ? "on":"off";
echo "[*] allow_url_fopen: ${auo}\n";

$tmp = sys_get_temp_dir();
echo "[*] tmp dir: ${tmp}\n";

$fso = function_exists('fsockopen') ? "enabled":"disabled";
echo "[*] fsockopen: ${fso}\n";

$curl = function_exists('curl_version') ? "enabled":"disabled";
echo "[*] curl: ${curl}\n";

$mail = function_exists('mail') ? "enabled":"disabled";
echo "[*] mail: ${mail}\n";

$er = (ini_get('error_reporting')!=0) ? "on":"off";
echo "[*] error_reporting: ${er}\n";

$de = (ini_get('display_errors')==1) ? "on":"off";
echo "[*] display_errors: ${de}\n";

$met = ini_get('max_execution_time');
echo "[*] max_execution_time: ${met}s\n";

$ml = ini_get('memory_limit');
echo "[*] memory_limit: ${ml}\n";

$dst = ini_get('default_socket_timeout');
echo "[*] default_socket_timeout: ${dst}s\n";

$upl = (ini_get('file_uploads')==1) ? "enabled":"disabled";
echo "[*] file_uploads: ${upl}\n";

$umf = ini_get('upload_max_filesize');
echo "[*] upload_max_filesize: ${umf}\n";

$dfs = ini_get('disable_functions');
if ($dfs != '') {
    echo "[!] disable_functions:\n";
    foreach(explode(',', $dfs) as $df) {
        if (trim($df) != '') {
            echo "[-] $df\n";
        }
    }
}
