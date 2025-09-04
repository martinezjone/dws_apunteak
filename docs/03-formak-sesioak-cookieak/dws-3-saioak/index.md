# Saioak (Sesiones)

Saioek webgune batean erabiltzailearen egoera gordetzeko aukera ematen dute. Atal honetan ikusiko dugu nola erabili PHP-n saioak erabiltzailearen informazioa gordetzeko eta kudeatzeko.

## Zer dira saioak?

Saio bat erabiltzaile baten informazioa gordetzeko mekanismo bat da, hainbat orrialdetan zehar mantentzen dena. PHP-k saioak automatikoki kudeatzen ditu cookie baten bidez.

## Saioak hasi

```php
<?php
// Saioa hasi
session_start();

// Aldagai bat gorde saioan
$_SESSION['erabiltzailea'] = 'ikaslea';
$_SESSION['rola'] = 'admin';
?>
```

## Saioaren datuak erabili

```php
<?php
// Saioa hasi (beharrezkoa da orrialde bakoitzean)
session_start();

// Datu bat erakutsi
if(isset($_SESSION['erabiltzailea'])) {
    echo 'Ongi etorri, ' . htmlspecialchars($_SESSION['erabiltzailea']);
}
?>
```

## Saioa itxi

```php
<?php
// Saioa hasi
session_start();

// Saio guztiz ezabatu
session_destroy();

// Berbideraketa egin
header('Location: index.php');
exit;
?>
```

## Segurtasuna

- Beti erabili `session_start()` saioarekin lan egin aurretik
- Erabili `htmlspecialchars()` erabiltzailearen sarrera bistaratzean
- Egiaztatu erabiltzaileak baimenak dituen orrialdeetara sartzeko
- Erabili HTTPS saioen cookie seguruak erabiltzeko
