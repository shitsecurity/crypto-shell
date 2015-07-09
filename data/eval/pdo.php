$db='$$ARGV1';
$username='$$ARGV2';
$password='$$ARGV3';
$query='$$ARGV4';

try {
    $dbh = new PDO("$db:host=127.0.0.1", $username, $password);
    $dbh->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    foreach ($dbh->query($query) as $row) {
        print "[*] ";
        for($ii=0; $ii<count($row)/2; $ii++) {
            print "$row[$ii]";
            if($ii!=count($row)/2-1) {
                print " | ";
            }
        }
        print "\n";
    }
}
catch(PDOException $e) {
    echo $e->getMessage();
}
