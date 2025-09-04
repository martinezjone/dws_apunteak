# Erabiltzaileen Kudeaketa

Atal honetan, web aplikazio batean erabiltzaileen erregistroa, saio-hasiera eta profil-kudeaketa nola inplementatu aztertuko dugu.

## 1. Erabiltzailearen Erregistroa

### Datuak jasotzeko formularioa
```html
<form action="erregistroa_prozesatu.php" method="post">
    <div>
        <label for="erabiltzailea">Erabiltzaile izena:</label>
        <input type="text" id="erabiltzailea" name="erabiltzailea" required>
    </div>
    
    <div>
        <label for="email">E-posta:</label>
        <input type="email" id="email" name="email" required>
    </div>
    
    <div>
        <label for="pasahitza">Pasahitza:</label>
        <input type="password" id="pasahitza" name="pasahitza" required>
    </div>
    
    <div>
        <label for="pasahitza_berretsi">Pasahitza berretsi:</label>
        <input type="password" id="pasahitza_berretsi" name="pasahitza_berretsi" required>
    </div>
    
    <button type="submit">Erregistratu</button>
</form>
```

### Erregistroa prozesatzeko kodea
```php
<?php
// Datu basearen konexioa
require_once 'db_connect.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Datuak garbitu eta balioztatu
    $erabiltzailea = filter_input(INPUT_POST, 'erabiltzailea', FILTER_SANITIZE_STRING);
    $email = filter_input(INPUT_POST, 'email', FILTER_SANITIZE_EMAIL);
    $pasahitza = $_POST['pasahitza'];
    $pasahitza_berretsi = $_POST['pasahitza_berretsi'];
    
    // Balidazioa
    $erroreak = [];
    
    if (empty($erabiltzailea) || strlen($erabiltzailea) < 3) {
        $erroreak[] = "Erabiltzaile izenak gutxienez 3 karaktere izan behar ditu";
    }
    
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $erroreak[] = "E-posta helbidea ez da baliozkoa";
    }
    
    if (strlen($pasahitza) < 8) {
        $erroreak[] = "Pasahitzak gutxienez 8 karaktere izan behar ditu";
    } elseif ($pasahitza !== $pasahitza_berretsi) {
        $erroreak[] = "Pasahitzak ez datoz bat";
    }
    
    // Erabiltzaile izena eta eposta errepikatuta egon daitezkeen egiaztatu
    $stmt = $pdo->prepare("SELECT COUNT(*) FROM erabiltzaileak WHERE erabiltzailea = ? OR email = ?");
    $stmt->execute([$erabiltzailea, $email]);
    
    if ($stmt->fetchColumn() > 0) {
        $erroreak[] = "Erabiltzaile izena edo e-posta helbidea jadanik erregistratuta dago";
    }
    
    // Erroreak badaude, erakutsi
    if (!empty($erroreak)) {
        foreach ($erroreak as $errorea) {
            echo "<p>Errorea: $errorea</p>";
        }
    } else {
        // Erabiltzailea sortu
        $pasahitz_hash = password_hash($pasahitza, PASSWORD_DEFAULT);
        $stmt = $pdo->prepare("INSERT INTO erabiltzaileak (erabiltzailea, email, pasahitza) VALUES (?, ?, ?)");
        
        if ($stmt->execute([$erabiltzailea, $email, $pasahitz_hash])) {
            echo "Erregistroa ondo burutu da. Orain saioa hasi dezakezu.";
            header('Location: saioa_hasi.php');
            exit;
        } else {
            echo "Errorea erregistroa egitean. Saia zaitez berriro geroago.";
        }
    }
}
?>
```

## 2. Saio-hasiera

### Saioa hasteko formularioa
```html
<form action="saioa_hasi.php" method="post">
    <div>
        <label for="erabiltzailea">Erabiltzaile izena:</label>
        <input type="text" id="erabiltzailea" name="erabiltzailea" required>
    </div>
    
    <div>
        <label for="pasahitza">Pasahitza:</label>
        <input type="password" id="pasahitza" name="pasahitza" required>
    </div>
    
    <div>
        <input type="checkbox" id="gogoratu" name="gogoratu">
        <label for="gogoratu">Gogoratu nire saioa</label>
    </div>
    
    <button type="submit">Sartu</button>
</form>
```

### Saioa hasteko kodea
```php
<?php
session_start();
require_once 'db_connect.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $erabiltzailea = filter_input(INPUT_POST, 'erabiltzailea', FILTER_SANITIZE_STRING);
    $pasahitza = $_POST['pasahitza'];
    $gogoratu = isset($_POST['gogoratu']) ? true : false;
    
    // Erabiltzailea bilatu datu basean
    $stmt = $pdo->prepare("SELECT * FROM erabiltzaileak WHERE erabiltzailea = ?");
    $stmt->execute([$erabiltzailea]);
    $erabiltzailea_db = $stmt->fetch();
    
    if ($erabiltzailea_db && password_verify($pasahitza, $erabiltzailea_db['pasahitza'])) {
        // Saioa hasi
        $_SESSION['erabiltzailea_id'] = $erabiltzailea_db['id'];
        $_SESSION['erabiltzailea'] = $erabiltzailea_db['erabiltzailea'];
        $_SESSION['rola'] = $erabiltzailea_db['rola'] ?? 'erabiltzailea';
        
        // Gogoratu nire saioa aukeratuta badago
        if ($gogoratu) {
            $token = bin2hex(random_bytes(32));
            $iraungitze_data = date('Y-m-d H:i:s', strtotime('+30 days'));
            
            // Token-a gorde datu basean
            $stmt = $pdo->prepare("UPDATE erabiltzaileak SET remember_token = ?, token_iraungitze_data = ? WHERE id = ?");
            $stmt->execute([$token, $iraungitze_data, $erabiltzailea_db['id']]);
            
            // Cookie-a ezarri
            setcookie('remember_me', $token, strtotime('+30 days'), '/', '', true, true);
        }
        
        // Berbideraketa
        header('Location: index.php');
        exit;
    } else {
        $errorea = "Erabiltzaile izena edo pasahitza okerra";
    }
}
?>
```

## 3. Profilaren Kudeaketa

### Profila erakutsi
```php
<?php
session_start();
require_once 'db_connect.php';

// Egiaztatu erabiltzailea saioa hasita dagoen
if (!isset($_SESSION['erabiltzailea_id'])) {
    header('Location: saioa_hasi.php');
    exit;
}

// Erabiltzailearen datuak lortu
$stmt = $pdo->prepare("SELECT * FROM erabiltzaileak WHERE id = ?");
$stmt->execute([$_SESSION['erabiltzailea_id']]);
$erabiltzailea = $stmt->fetch();
?>

<h1>Nire Profila</h1>
<p>Erabiltzailea: <?php echo htmlspecialchars($erabiltzailea['erabiltzailea']); ?></p>
<p>E-posta: <?php echo htmlspecialchars($erabiltzailea['email']); ?></p>
<p>Erregistro data: <?php echo date('Y-m-d', strtotime($erabiltzailea['sortze_data'])); ?></p>

<h2>Pasahitza aldatu</h2>
<form action="pasahitza_aldatu.php" method="post">
    <div>
        <label for="egungo_pasahitza">Uneko pasahitza:</label>
        <input type="password" id="egungo_pasahitza" name="egungo_pasahitza" required>
    </div>
    
    <div>
        <label for="pasahitz_berria">Pasahitz berria:</label>
        <input type="password" id="pasahitz_berria" name="pasahitz_berria" required>
    </div>
    
    <div>
        <label for="pasahitz_berria_berretsi">Pasahitz berria berretsi:</label>
        <input type="password" id="pasahitz_berria_berretsi" name="pasahitz_berria_berretsi" required>
    </div>
    
    <button type="submit">Pasahitza aldatu</button>
</form>
```

### Pasahitza aldatzeko kodea
```php
<?php
session_start();
require_once 'db_connect.php';

if (!isset($_SESSION['erabiltzailea_id'])) {
    header('Location: saioa_hasi.php');
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $egungo_pasahitza = $_POST['egungo_pasahitza'];
    $pasahitz_berria = $_POST['pasahitz_berria'];
    $pasahitz_berria_berretsi = $_POST['pasahitz_berria_berretsi'];
    
    // Egiaztatu pasahitz berriak bat datozela
    if ($pasahitz_berria !== $pasahitz_berria_berretsi) {
        $errorea = "Pasahitz berriak ez datoz bat";
    } elseif (strlen($pasahitz_berria) < 8) {
        $errorea = "Pasahitz berriak gutxienez 8 karaktere izan behar ditu";
    } else {
        // Egiaztatu uneko pasahitza zuzena den
        $stmt = $pdo->prepare("SELECT pasahitza FROM erabiltzaileak WHERE id = ?");
        $stmt->execute([$_SESSION['erabiltzailea_id']]);
        $erabiltzailea = $stmt->fetch();
        
        if (password_verify($egungo_pasahitza, $erabiltzailea['pasahitza'])) {
            // Eguneratu pasahitza
            $pasahitz_hash = password_hash($pasahitz_berria, PASSWORD_DEFAULT);
            $stmt = $pdo->prepare("UPDATE erabiltzaileak SET pasahitza = ? WHERE id = ?");
            
            if ($stmt->execute([$pasahitz_hash, $_SESSION['erabiltzailea_id']])) {
                $mezua = "Pasahitza ondo aldatu da";
            } else {
                $errorea = "Errorea pasahitza aldatzean";
            }
        } else {
            $errorea = "Uneko pasahitza ez da zuzena";
        }
    }
}

// Errore bat balego, erakutsi
if (isset($errorea)) {
    echo "<p>Errorea: $errorea</p>";
}

// Mezua balego, erakutsi
if (isset($mezua)) {
    echo "<p>$mezua</p>";
}
?>
```

## 4. Saioa itxi

```php
<?php
session_start();

// Saio guztiz ezabatu
$_SESSION = array();

// Cookie-a ezabatu
if (ini_get("session.use_cookies")) {
    $params = session_get_cookie_params();
    setcookie(session_name(), '', time() - 42000,
        $params["path"], $params["domain"],
        $params["secure"], $params["httponly"]
    );
}

// Saioa suntsitu
session_destroy();

// Berbideraketa
header('Location: index.php');
exit;
?>
```
