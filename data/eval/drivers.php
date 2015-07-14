try {
    $drivers = PDO::getAvailableDrivers();
    if (count($drivers) == 0) {
        echo '[!] no drivers';
    } else {
        foreach($drivers as $driver) {
            echo "[*] $driver\n";
        }
    }
} catch(PDOException $e) {
    echo $e->getMessage();
}
