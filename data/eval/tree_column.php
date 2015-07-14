$db='$$ARGV1';
$username='$$ARGV2';
$password='$$ARGV3';

try {
    $dbh = new PDO("$db:host=127.0.0.1", $username, $password);
    $dbh->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $dbs = "show databases;";
    foreach ($dbh->query($dbs) as $db) {
        echo "[*] $db[0]\n";
        $tables = "show tables from $db[0];";
        foreach ($dbh->query($tables) as $table) {
            echo "[*] $db[0]::$table[0]\n";
            $columns = "show columns from $db[0].$table[0];";
            foreach ($dbh->query($columns) as $column) {
                echo "[*] $db[0]::$table[0]::$column[0]\n";
            }
        }
    }
}
catch(PDOException $e) {
    echo $e->getMessage();
}
