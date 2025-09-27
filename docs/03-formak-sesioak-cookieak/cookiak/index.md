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
        'nombre_cookie',       // nombre de la cookie
        'valor_cookie',        // valor de la cookie
        [
            'expires'  => time() + 3600,  // fecha de expiración (timestamp)
            'path'     => '/',            // path donde la cookie es válida
            'domain'   => 'tudominio.com',// dominio donde es válida
            'secure'   => true,           // solo HTTPS
            'httponly' => true,           // no accesible desde JavaScript
            'samesite' => 'Lax'           // 'Strict' | 'Lax' | 'None'
        ]
    );

```


## Cookien atributuak
Cookie batean honako atributuak defini daitezke:

    - **nombre_cookie**: Nombre identificador de la cookie
    - **valor_cookie**: Valor que se almacenará (string)
    - **expires**: Fecha de expiración (timestamp)
    - **path**: Path dentro del dominio donde la cookie es válida
    - **domain**: Dominio donde la cookie es válida
    - **secure**: Solo enviar cookie sobre HTTPS (true recomendado)
    - **httponly**: Evita que JS acceda a la cookie
    - **samesite**: Protege contra CSRF (Strict, Lax o None)


**Hona hemen adibide bat:**

```php
    
    setcookie('erabiltzaile', 'Aimar', [
        'expires'  => time() + 60*60,  // 60 minututan iraungiko da
        'path'     => '/cookies/',     // Cookie hau baliozko path honetan bakarrik
        'domain'   => 'Webestilo.com', // Cookie hau baliozko domeinuan bakarrik
        'secure'   => true,            // HTTPS soilik; segurtasuna handitzeko
        'httponly' => true,            // JavaScript-ek ezin du cookie honetara sarbiderik izan
        'samesite' => 'Lax'            // CSRF-ren aurkako babesa ('Strict', 'Lax' edo 'None')
    ]);

```
Hor, “erabiltzaile” cookie sortzen da, “Aimar” balioarekin, ordu bete iraungo duena eta domeinu horretakoa.

## Cookieak berreskuratu eta erabili
Cookie baten balioa irakurtzeko, `$_COOKIE[]` array asoziatiboa erabiltzen da, cookiaren izena erabilita:

```php
    if (isset($_COOKIE['nombre_cookie'])) {
        $valor = $_COOKIE['nombre_cookie'];
        // Escapamos antes de imprimir en HTML
        echo htmlspecialchars($valor, ENT_QUOTES, 'UTF-8');
    }

    // Gure adibidearekin jarraitzeko
    $erabiltzailea = $_COOKIE['erabiltzaile'];
    echo htmlspecialchars($erabiltzailea, ENT_QUOTES, 'UTF-8'); // Aimar bueltatzen du
```

Cooki baten datua aldatzeko:

```php
    setcookie(
        'nombre_cookie',
        'nuevo_valor', // Nuevo valor
        [
            'expires'  => time() + 7200,    // Nueva expiración
            'path'     => '/',
            'domain'   => 'tudominio.com',
            'secure'   => true,
            'httponly' => true,
            'samesite' => 'Lax'
        ]
    );

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
   setcookie(
        'nombre_cookie',
        '',
        [
            'expires'  => time() - 3600,    // Expiración en el pasado !!!!!!
            'path'     => '/',               // Mismo path que la original
            'domain'   => 'tudominio.com',  // Mismo dominio
            'secure'   => true,
            'httponly' => true,
            'samesite' => 'Lax'
        ]
    );
```

## Cookien mugak
- Cookien tamaina maximoa 4096Bytes da (4KB).
- Domeinu bakoitzeko gutxi gora-behera 20 cookie erakutsi daitezke, nabigatzailearen arabera.
- Diskoan 300 cookie maximo gordetzen dira, gehiago sartzen denean zaharrena ezabatzen da.


### Adibide osoa: Cookie berrezkuratzea eta iraungitzea
```php
    <?php
        // Cookie bat modu seguru batean sortzea
        setcookie('erabiltzaile', 'Homer', [
            'expires'  => time() + 60*30,  // 30 minututan iraungiko da
            'path'     => '/cookies/',     // Path honetan bakarrik balio du
            'domain'   => 'prueba.dev',   // Domeinu honetan bakarrik balio du
            'secure'   => true,            // HTTPS soilik; segurtasuna handitzeko
            'httponly' => true,            // JavaScript-ek ezin du cookie honetara sarbiderik izan
            'samesite' => 'Lax'            // CSRF-ren aurkako babesa ('Strict', 'Lax' edo 'None')
        ]);

        // Cookiea berreskuratzea eta modu seguruan erakustea
        if (isset($_COOKIE['erabiltzaile'])) {
            $balioCookie = $_COOKIE['erabiltzaile'];
            echo htmlspecialchars($balioCookie, ENT_QUOTES, 'UTF-8'); // XSS aurkako babesa
        }
    ?>
```

### Non gordetzen dira cookiak nabigatzailean?
- **Chrome:** Configuración > Privacidad y seguridad > Cookies de terceros > Ver todos los datos y permisos de sitios
- **Firefox:** Ajustes > Privacidad y seguridad > Cookies y datos del sitio > Administrar datos

## Ohar teknikoak eta best-practice-ak
- `setcookie` funtzioari deitu behar zaio HTMLaren edozein etiketa baino lehen.
- Behar diren atributuak soilik sartu.
- Domeinuko cookiak domeinu beretik soilik irakur daitezke.

## Segurtasun-oharrak

- Ez gorde informazio sentikorrik cookietan (pasahitzak, kreditu-txartelak...).
- Erabili `httponly` eta `secure` flag-ak.
- Ezarri `samesite` (gomendatua: `Strict` edo `Lax`) CSRFren aurka.
- Erabili `htmlspecialchars()` erabiltzaileari cookie balioak bistaratzean.
- HTTPS erabili; `SameSite=None` bada, derrigorrezkoa da `secure`.


!!! exercise "Ariketa 10"
    - [ ] Eginda dut
    
    Sortu formulario bat eta bertan erabiltzaileari izena eskatu. Izena cookie batean gorde, eta cookiearen balioa pantailaratu.
    Fitxategi bakar baten egin.

!!! exercise "Ariketa 11"
    - [ ] Eginda dut
    
    “azken_saio” izeneko cookie sortuta dagoen egiaztatu. Ez badago, sortu, eta eguna + ordua gorde (date('Y-m-d H:i:s')). Sortuta balego, pantailaratu sarrera aurreko momentua eta eguneratu.