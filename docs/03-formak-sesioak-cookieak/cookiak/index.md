# Cookiak

Cookiak erabiltzailearen nabigatzailean gordetzen diren testu fitxategi txikiak dira. Hauek erabiltzailearen informazioa gordetzeko erabiltzen dira, hala nola saio-hasierak, hobespenak edo jarraipena egiteko.

## Cookie bat sortu PHP-n

```php
<?php
// Cookie bat sortu 30 egunetarako
$izena = "erabiltzailea";
$balioa = "ikasle123";
$iraungitze_data = time() + (86400 * 30); // 30 egun
setcookie($izena, $balioa, $iraungitze_data, "/");
?>
```

## Cookie bat irakurri

```php
<?php
if(isset($_COOKIE['erabiltzailea'])) {
    echo "Erabiltzailearen izena: " . htmlspecialchars($_COOKIE['erabiltzailea']);
} else {
    echo "Ez da cookierik aurkitu";
}
?>
```

## Cookie bat ezabatu

```php
<?php
// Cookie bat ezabatzeko, iraungitze-data iraganera ezarri
setcookie("erabiltzailea", "", time() - 3600, "/");
?>
```

## Segurtasun-oharrak

- Ez gorde informazio sentikorrik cookietan (pasahitzak, kreditu-txartel zenbakiak, etab.)
- Erabili `httponly` eta `secure` flag-ak segurtasunerako
- Erabili `samesite` atributua CSRF erasoen aurka babesteko
- Beti egiaztatu erabiltzailearen sarrera

## Adibide osoa

```php
<?php
// Cookie bat sortu
$erabiltzailea = "ikasle456";
setcookie("erabiltzailea", $erabiltzailea, time() + (86400 * 30), "/", "", true, true);

// Cookie bat irakurri
if(isset($_COOKIE['erabiltzailea'])) {
    echo "Ongi etorri berriz, " . htmlspecialchars($_COOKIE['erabiltzailea']);
}
?>
```
