# Cookiak

## Zer diren eta zertarako erabiltzen diren

Cookieak datu zati txikiak dira, webgune batek erabiltzailearen nabigatzailean gordetzen dituenak, etorkizunean informazioa berreskuratzeko. HTTP eta HTTPS estaturik gabeko protokoloak dira; zerbitzariak eta bezeroak ez dute orrialde batetik bestera datuen jarraipenik egiten, unless forms are used. Cookieek eta saioek informazioa orrien artean pasatzeko aukera ematen dute.

## Cookieen funtzionamendua
Cookien bidez, webguneek bisitarien informazioa lokal gordetzen dute: erabiltzaile izenak, hizkuntza, saioaren egoera, bisita ohikoak etab. Aldiz, saioaren datuak zerbitzarian gordetzen dira; cookienak, bezeroaren diskoan.

- Cookieak erabiltzen badira, baliteke erabiltzaileak hauek desaktibatzea eta aplikazioak ez funtzionatzea.
- Saioak erabiltzen badira bisitari asko izatean, zerbitzaria kargatu daiteke.

## Cookie bat nola sortu PHPn
Cookie bat bidaltzeko, setcookie() funtzioa erabiltzen da. Cookieak header zatian bidali behar dira, HTML tag-ak baino lehen. Sintaxia hau da:

```php
    setcookie(
        izena, 
        balioa, 
        iraungitze_data, 
        path, 
        domain, 
        secure
    );
```

Hona hemen adibide bat:

```php
    setcookie("erabiltzaile", "Aimar", time() + 3600, "/", "Webestilo.com");
```
Hor, “erabiltzaile” cookie sortzen da, “Aimar” balioarekin, ordu bete iraungo duena eta domeinu horretakoa.

## Cookieak berreskuratu eta erabili
Cookie baten balioa irakurtzeko, `$_COOKIE[]` array asoziatiboa erabiltzen da, cookiaren izena erabilita:

```php
    $balioa = $_COOKIE['erabiltzaile'];
    echo $balioa; // Aimar bueltatzen du
```

Cookie bat *existitzen den egiaztatzeko*, `isset()` funtzioa erabili dezakegu:

```php
    if(isset($_COOKIE['cookie_izena'])) {
        echo "<p>Cookia sortuta izan da</p>";
    } else {
        echo "<p>Cookia ez da existitzen</p>";
    }
```

Cookie bat *ezabatzeko*, iraungitze-data atzera jarri behar da:

```php
    setcookie('cookie1', 'valorcookie1', time() - 60);
```

## Cookien atributuak
Cookie batean honako atributuak defini daitezke:

- *name*: cookiaren izena.
- *value*: gordetuko den balioa.
- *expires*: cookiearen iraungitze data.
- *path*: webgunearen zein bideetan erabilgarri den.
- *domain*: domeinua (zerbitzariari lotuta).
- *secure*: HTTP edo HTTPS erabileraren arabera (true = HTTPS bakarrik).

## Cookien mugak
- Cookien tamaina maximoa 4096Bytes da (4KB).
- Domeinu bakoitzeko gutxi gora-behera 20 cookie erakutsi daitezke, nabigatzailearen arabera.
- Diskoan 300 cookie maximo gordetzen dira, gehiago sartzen denean zaharrena ezabatzen da.


!!! exercise "Ariketa 9"
    - [ ] Eginda dut
    
    Sortu formulario bat eta bertan erabiltzaileari izena eskatu. Izena cookie batean gorde, eta cookiearen balioa pantailaratu.

!!! exercise "Ariketa 10"
    - [ ] Eginda dut
    
    “azken_saio” izeneko cookie sortuta dagoen egiaztatu. Ez badago, sortu, eta eguna + ordua gorde (date('Y-m-d H:i:s')). Sortuta balego, pantailaratu sarrera aurreko momentua eta eguneratu.

### Adibide osoa: Cookie berrezkuratzea eta iraungitzea
```php
    setcookie('usuario', 'Homer', time() + 60*30, '/cookies/', 'prueba.dev', false, true);
    if (isset($_COOKIE['usuario'])) {
        $valorCookie = $_COOKIE['usuario'];
        echo $valorCookie; // Homer bueltatzen du
    }
```

### Non gordetzen dira cookiak nabigatzailean?
*Chrome:* Configuración > Privacidad y seguridad > Cookies de terceros > Ver todos los datos y permisos de sitios
*Firefox:* Ajustes > Privacidad y seguridad > Cookies y datos del sitio > Administrar datos

## Ohar teknikoak eta best-practice-ak
- Setcookie funtzioari deitu behar zaio HTMLaren edozein etiketa baino lehen.
- Behar diren atributuak soilik sartu.
- Domeinuko cookiak domeinu beretik soilik irakur daitezke.

## Segurtasun-oharrak

- Ez gorde informazio sentikorrik cookietan (pasahitzak, kreditu-txartelak...).
- Erabili `httponly` eta `secure` flag-ak.
- Ezarri `samesite` (gomendatua: `Strict` edo `Lax`) CSRFren aurka.
- Erabili `htmlspecialchars()` erabiltzaileari cookie balioak bistaratzean.
- HTTPS erabili; `SameSite=None` bada, derrigorrezkoa da `secure`.
“azken_saio” izeneko cookie sortuta dagoen egiaztatu. Ez badago, sortu, eta eguna + ordua gorde (date('Y-m-d H:i:s')). Sortuta balego, pantailaratu sarrera aurreko momentua eta eguneratu.
