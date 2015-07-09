$db='$$ARGV1';
$username='$$ARGV2';
$password='$$ARGV3';
$dbname='$$ARGV4';
$table='$$ARGV5';

try {
    $dbh = new PDO("$db:host=127.0.0.1", $username, $password);
    $dbh->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $columns = "show columns from $dbname.$table;";
    foreach ($dbh->query($columns) as $column) {
        echo "[*] $dbname::$table::$column[0]\n";
    }
}
catch(PDOException $e) {
    echo $e->getMessage();
}
