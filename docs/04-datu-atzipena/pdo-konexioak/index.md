# PDO konexioak Web garapena zerbitzari-ingurunean Konexioa (PDO)

PDO (PHP Data Objects) datu-baseak kudeatzeko hainbat sistemarekin (MySQL, PostgreSQL eta SQLite, besteak beste) elkarreragiteko interfaze bateratua eskaintzen duen PHP luzapena da. MySQL funtzio espezifikoak ez bezala (mysqli_ bezala), PDO ez dago datu-base mota bakar batera mugatuta. 

Horrek esan nahi du, PDOrekin, datu-base sistema batetik bestera alda zaitezkeela kode asko berridatzi behar izan gabe. PDOk garatzaileei aukera ematen die datu-baseekin konektatzeko eta eragiketak egiteko interfaze komun baten bidez, erabiltzen ari zaren datu-base mota edozein dela ere. Beraz, hau egin dezakezu: Datu-basera konektatzeko, SQL kontsultak.

## Konexioa sortu
Lehenengo gauza egingo duguna datu base batekin lan egin ahal izateko, konexioa sortzea izango da. Horretarako PDO objektu bat sortuko dugu hurrengo parametroekin:

```php
    $hostDB = '127.0.0.1'
    $nombreDB = 'DB_adibidea'
    $usuarioDB = 'root'
    $contrasenyaDB = ''

    $dsn = "mysql:host=$hostDB;dbname=$nombreDB;charset=utf8mb4"
    $options = [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        PDO::ATTR_EMULATE_PREPARES => false,
    ]

    try {
        $pdo = new PDO($dsn, $usuarioDB, $contrasenyaDB, $options)
    } catch (PDOException $e) {
        error_log('DB konexio errorea: ' . $e->getMessage())
        die('Ezin izan da datu-basearekin konektatu.')
    }
```

    • `$dsn`: (data source name) - Datu-base mota (kasu honetan, MySQL), ostalaria eta datu-basearen izena zehazten ditu.
    • `$username`: DBko erabilzailea.
    • `$password`: DBko pasahitza.
    • `$options`: konexioak behar ditzakeen parametro gehigarrien zerrenda (adibidez, erroreen modua, datuak itzultzeko modua, etab.).

Honekin lortzen duguna da PDO objektuaren instantzia bat sorraraztea; beraz behin sortuta dugunean objektu horren metodoak eta propietateak erabili ditzakegu.

`DSN`-k hurrengo estruktura izango du:

```php
    $dsn = 'mysql:host=DBHOST;port=DBPORT;dbname=DBNAME';
```
    • `$mysql`: zein DB driverra erabiliko den esaten da, gure kasuan MySql.
    • `$DBHOST`: datu-basearen zerbitzariaren hostname edo IP definitzen du.
    • `$DBPORT`: konexiorako portua, MySQLn lehenetsitako portua 3306 da, beraz ez da derrigorrezkoa jartzea.
    • `$DBNAME`: DB-aren izena.

Gure kasuan, lokalean egingo dugunez lan, hurrengo datuak jarri beharko ditugu:

```php
    //Hauek dira erabiliko ditugun aldagaiak
    $hostDB = '127.0.0.1'; //localhost
    $nombreDB = 'DB_adibidea';
    $usuarioDB = 'root';
    $contrasenyaDB = '';
```

## Kontsultak (PDO)

PDOk kontsultak egiteko bi metodo nagusi eskaintzen ditu, bakoitza bere erabilerarekin:

### 1. `query`

- SQL zuzenean exekutatzen du.
- Egokia kontsulta sinpleentzat, parametro barik edo beti seguruak direnentzat.
- Ez da gomendagarria erabiltzaileko sarrera duten kontsultetarako, SQL Injection arriskua dela eta.

```php
    $sql = "SELECT * FROM libros WHERE categoria = 'Históricos'";
    $stmt = $pdo->query($sql);
    $emaitzak = $stmt->fetchAll();
```

!!! info "Oharra"
    - `$pdo` PDO objektua da, datu-base konexioa.
    - `$stmt` PDOStatement objektua da, kontsultaren emaitzak gordetzen dituena.
    - `$emaitzak` array asoziatiboa da, datu guztiak jasotzen dituena.

### 2. `prepare` + `execute`

- Kontsulta bat prestatu eta gero exekutatu parametroren bat erabiliz.
- Segurua da, erabiltzaileko inputak SQL Injection saihesteko.
- Beren balioak aldatuta hainbat aldiz erabil daitezke, parametro berdinak edo desberdinak erabiliz.

```php
    $sql = "SELECT * FROM usuarios WHERE nombre = :nombre";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':nombre', $nombre);
    $stmt->execute();
    $usuario = $stmt->fetch();
```

!!! info "Oharra"
    - `$sql` kontsulta zuzena.
    - `$stmt` PDOStatement objektua da, kontsultaren emaitzak gordetzen dituena.
    - `$usuario` array asoziatiboa da, datu guztiak jasotzen dituena.

## Parametroak pasatzeko hiru moduak

PDOk hiru modu nagusi eskaintzen ditu prepared statements-era parametroak pasatzeko:

### 1. `bindParam`

- Aldagaiaren erreferentzia lotzen du.
- `execute()` garaian aldagaiaren balioa hartzen du.
- Balioa exekutatu aurretik alda daiteke, eta aldatutako balioa erabiliko da.

```php
    $valor = "Hasierako balioa";
    $stmt = $pdo->prepare("INSERT INTO tabla (columna) VALUES (:valor)");
    $stmt->bindParam(':valor', $valor);
    $valor = "Balio berria"; // Honek aldatuko du exekutatutako kontsultaren balioa.
    $stmt->execute();
```

### 2. `bindValue`

- Balioa berehala lotzen du.
- Aldagaiaren balioa aldatu arren, exekutatu aurretik sortutako balioa erabiltzen du.

```php
    $valor = "Hasierako balioa";
    $stmt = $pdo->prepare("INSERT INTO tabla (columna) VALUES (:valor)");
    $stmt->bindValue(':valor', $valor);
    $valor = "Balio berria"; // EZ DU eragingo exekutatzen den balioan
    $stmt->execute();
```

### 3. `execute` + array

- Modu erosoena eta gomendagarriena.
- Parameter guztiak `execute()`-ri array bat pasatuz ematen zaizkio.

```php
    $stmt = $pdo->prepare("INSERT INTO tabla (columna1, columna2, columna3) VALUES (:valor1, :valor2, :valor3)");
    $parametros = [
        ':valor1' => "Valor 1",
        ':valor2' => "Valor 2",
        ':valor3' => "Valor 3",
    ];
$stmt->execute($parametros);
```

## Kontsultak emandako emaitzak jasaotzeko
PDOk metodo pare bat eskeintzen ditu kontsultak emandako emaitzak ezagutzeko:

### 1.  **`fetch`**: 
    - Emaitzen hurrengo erregistroa lortzen du. Banan banan erakusten ditu, ez direnean gehiago gelditzen `false` ematen du.

```php
    $stmt = $pdo->prepare("SELECT nombre, edad FROM personas");
    $stmt->execute();
    while ($fila = $stmt->fetch()) {
    echo "Nombre: " . $fila['nombre'] . ", Edad: " . $fila['edad'] . "<br>";
    }
```

### 2.  **`fetchAll`**: 
    - Emaitzen erregistro guztiak dituen array bat lortzen du.

```php
    $stmt = $pdo->prepare("SELECT nombre, edad FROM personas");
    $stmt->execute();
    $resultados = $stmt->fetchAll();
    foreach ($resultados as $fila) {
    echo "Nombre: " . $fila['nombre'] . ", Edad: " . $fila['edad'] . "<br>";
    }
```

### 3. `fetchAll()` erabili barik `foreach` bidez erregistroak lortzea:

```php
    $stmt = $pdo->prepare("SELECT nombre, edad FROM personas");
    $stmt->execute();
    foreach ($stmt as $fila) {
    echo "Nombre: " . $fila['nombre'] . ", Edad: " . $fila['edad'] . "<br>";
    }
```

    fetchAll() erabili barik - foraech-ek Filak banan banan jasotzen ditugu, ez dugu dena memorian gordetzen

!!! info "Noiz erabili bata edo bestea?"
    Normalean datu gutxi jasoko baldin baditugu `fetchAll` erabili dezakegu bestela memoria asko erabiliko luke, `fetch`-ekin lan egitea kasu horieta eraginkorrago izango litzateke.


## Fetch moduak
| Mode | Deskribapena |
|------|--------------|
| `PDO::FETCH_ASSOC` | Array asoziatiboa, `$fila['nombre']` |
| `PDO::FETCH_NUM` | Array numerikoa, `$fila[0]` |
| `PDO::FETCH_BOTH` | Biak, `$fila[0]` edo `$fila['id']` |
| `PDO::FETCH_OBJ` | Objektua, `$fila->nombre` |
| `PDO::FETCH_CLASS` | Zure klasea, `$persona->edad` |
| `PDO::FETCH_COLUMN` | Zutabe bakarra, `["Jon", "Ane"]` |
| `PDO::FETCH_KEY_PAIR` | Gako → Balio, `[1 => "Jon"]` |
| `PDO::FETCH_GROUP` | Gako → Array multzoa |
| `PDO::FETCH_UNIQUE` | Gako bakarrak |

```php
    // FETCH_ASSOC - Emaitzak array asoziatibo moduan itzultzen ditu (gakoak zutabeen izenak dira).
    // Gehien erabiltzen dena da, oso garbia baita.

    $stmt = $pdo->query("SELECT id, nombre, edad FROM personas");
    while ($fila = $stmt->fetch(PDO::FETCH_ASSOC)) {
        echo $fila['id'] . " - " . $fila['nombre'] . " (" . $fila['edad'] . ")<br>";
    }

    // Emaitza:
    // 1 - Jon (25)
    // 2 - Ane (30)

    // FETCH_NUM - Emaitzak array numeriko moduan itzultzen ditu (gakoak zenbakiak dira).
    
    $stmt = $pdo->query("SELECT id, nombre, edad FROM personas");
    while ($fila = $stmt->fetch(PDO::FETCH_NUM)) {
        echo $fila[0] . " - " . $fila[1] . " (" . $fila[2] . ")<br>";
    }

    // Emaitza:
    // 1 - Jon (25)
    // 2 - Ane (30)

    // FETCH_BOTH - Emaitzak biak batera itzultzen ditu: gako numerikoekin eta asoziatiboekin.
    // Hau da, $fila[0] eta $fila['id'] berdinak izango dira.
    // Normalean ez da oso gomendagarria, memoria gehiago erabiltzen duelako.

    $stmt = $pdo->query("SELECT id, nombre FROM personas");
    $fila = $stmt->fetch(PDO::FETCH_BOTH);
    echo $fila[0];       // id
    echo $fila['nombre']; // nombre


    // FETCH_OBJ - Emaitzak objektu moduan itzultzen ditu (gakoak objektuaren atributuak dira).

    $stmt = $pdo->query("SELECT nombre, edad FROM personas");
    while ($fila = $stmt->fetch(PDO::FETCH_OBJ)) {
        echo $fila->nombre . " (" . $fila->edad . ")<br>";
    }

    // Emaitza:
    // Jon (25)
    // Ane (30)
```

## Erroreen kudeaketa PDOrekin

PDO erabiliz datu-basearekin lan egiten dugunean, erroreak modu egokian kudeatzea oso garrantzitsua da. Horretarako, PDO objektua sortzerakoan ATTR_ERRMODE aukera ezartzea komeni da.

```php
    $options = [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, // Salbuespenak jaurtiko ditu
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC // Emaitzak array asoziatibo gisa
    ];
    $pdo = new PDO($dsn, $username, $password, $options);
```

### Erroreen moduak
PDOk hiru errore-modu nagusi eskaintzen ditu:

| Modua | Deskribapena | Oharrak |
|-------|--------------|---------|
| `PDO::ERRMODE_SILENT` | Lehenetsia | Ez du errore-mezurik ematen; erroreak eskuz kudeatu behar dira `$pdo->errorInfo()` erabiliz |
| `PDO::ERRMODE_WARNING` | Abisuak ematen ditu (PHP warning) | Erroreak ikusi daitezke, baina ez da gelditzen exekuzioa |
| `PDO::ERRMODE_EXCEPTION` | Salbuespenak jaurtitzen ditu | Gomendagarriena; try/catch blokeetan detektatu daitezke eta exekuzioa kontrolpean gelditzen da |

### Adibide praktikoa

```php
    $dsn = "mysql:host=127.0.0.1;dbname=DB_adibidea;charset=utf8mb4";
    $username = 'root';
    $password = '';
    $options = [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, // Salbuespenak jaurtiko ditu
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC // Emaitzak array asoziatibo gisa
    ];

    try {
        $pdo = new PDO($dsn, $username, $password, $options);
        echo "Konexioa ondo burutu da.";
    } catch (PDOException $e) {
        echo "Errorea datu-basearekin konektatzerakoan: " . $e->getMessage();
    }
```


!!! warning "Oharrak"
    `PDO::ERRMODE_EXCEPTION` erabiltzea gomendatzen da beti, garapen fasean akatsak modu errazean detektatzeko eta produkzioan try/catch blokeak erabiliz kontrolatzeko.

## Transakzioak

Transakzio bat datu-basean burutzen den eragiketa-multzo atomikoa da: edo guztia egiten da (commit) edo ezer ez egiten da (rollback).
**Helburua:** datuen koherentzia eta kontzistentzia bermatzea, batez ere eragiketa anitz bateratu behar direnean (adib.: diru-transferentziak).

### PDOn transakzio oinarrizko metodoak

- `beginTransaction()` — transakzioa hasteko.
- `commit()` — transakzioan egindako aldaketak konfirmatzeko.
- `rollBack()` — transakzioa atzera botatzeko (aldaketak ez egiteko).
- `inTransaction()` — egungo PDO objektuak transakzio batean dagoen jakiteko (bool).

!!!info "Oharrak"
    `PDO::ATTR_ERRMODE` `PDO::ERRMODE_EXCEPTION` jartzea gomendatzen da, erroreak jasotzeko salbuespenen bidez.

### Oinarrizko adibidea: diru-transferentzia

Bi kontu daude: kontu A-tik dirua kendu eta kontu B-ra gehitu. Bi eragiketa hauek biak egin behar dira edo biek bertan behera:

```php
    try {
        $pdo->beginTransaction();

        $stmt = $pdo->prepare("UPDATE cuentas SET saldo = saldo - :monto WHERE id = :id");
        $stmt->execute([':monto' => 100, ':id' => $cuentaOrigen]);

        // Kontuaren saldoa egiaztatu nahi baduzu lehen edo txandakatu
        $stmt = $pdo->prepare("UPDATE cuentas SET saldo = saldo + :monto WHERE id = :id");
        $stmt->execute([':monto' => 100, ':id' => $cuentaDestino]);

        $pdo->commit();
    } catch (Exception $e) {
        // Zalantzarik gabe, atzera bota transakzioa
        if ($pdo->inTransaction()) {
            $pdo->rollBack();
        }
        throw $e; // edo log-eztatu eta mezua erakutsi
    }
```

!!!info "Zergatik erabili try/catch?"
    Errore bat gertatzen bada eta ez bazaizu rollback deitzen, datu-baseak egoera inkonsistentean gelditu daiteke. beginTransaction() egin ondoren beti jarri try/catch eta rollBack() errore kasuan.

!!! exercise Ariketa 1: Datu base baten konexioa sortu
    - [ ] Eginda dut

    1. Sortu `conexion.php` fitxeroa.
    2. Fitxero honetan `connectDB()` funtzioa sortu beharko dugu, funtzio honi datu-basearen izena bakarrik pasatuko diogu, PDO objektua itzuliko du.

    3. Ondoren, beste PHP fitxero bat sortuko dugu, erabiltzaile guztien datuak lortzeko, horretarako:
        - `conexion.php` inportatuko dugu `connectDB()` funtzioa erabili ahal izateko.
    
    4. Hau guztia egin ahal izateko datu base bat sortuko dugu phpMyAdmin erabiliz. Fitxategi honetan taula sortzeko kodea duzue: <a href="https://docs.google.com/document/d/1e_X_wF_RQcEdPKzFklU9JXF7GAUinlBSHf7CS-57LWA/edit?usp=sharing">CREATE TABLE USERS</a>
    
    
