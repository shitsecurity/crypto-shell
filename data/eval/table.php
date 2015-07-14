$db='$$ARGV1';
$username='$$ARGV2';
$password='$$ARGV3';
$dbname='$$ARGV4';

try {
    $dbh = new PDO("$db:host=127.0.0.1", $username, $password);
    $dbh->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $tables = "show tables from $dbname;";
    foreach ($dbh->query($tables) as $table) {
        echo "[*] $dbname::$table[0]\n";
    }
}
catch(PDOException $e) {
    echo $e->getMessage();
}
