$username='$$ARGV1';
$password='$$ARGV2';
$db='mysql';

try {
    $dbh = new PDO("$db:host=127.0.0.1;dbname=mysql", $username, $password);
    $dbh->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $dbs = "select user,password from mysql.user;";
    foreach ($dbh->query($dbs) as $creds) {
        echo "[*] ${creds['user']}:${creds['password']}\n";
    }
}
catch(PDOException $e) {
    echo $e->getMessage();
}
