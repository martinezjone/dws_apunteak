# Web Aplikazioen Segurtasuna

Web aplikazioak garatzean, segurtasuna lehenetsi beharreko kontzeptu garrantzitsua da. Atal honetan, ohiko segurtasun arazoak eta hauek nola konpondu aztertuko ditugu.

## 1. XSS (Cross-Site Scripting)

### Arazoa
Erabiltzailearen sarrera zuzenki bistaratzean kodea exekuta daiteke.

### Konponbidea
```php
<?php
// Txarrezkoa
echo $_POST['komentarioa'];

// Ongi
// htmlspecialchars erabili HTML karaktereak kodetzeko
echo htmlspecialchars($_POST['komentarioa'], ENT_QUOTES, 'UTF-8');
?>
```

## 2. SQL Injekzioa

### Arazoa
```sql
SELECT * FROM erabiltzaileak WHERE erabiltzailea = '$erabiltzailea' AND pasahitza = '$pasahitza';
```

### Konponbidea: Prepared Statements
```php
<?php
$stmt = $pdo->prepare("SELECT * FROM erabiltzaileak WHERE erabiltzailea = :erabiltzailea");
$stmt->execute(['erabiltzailea' => $erabiltzailea]);
$erabiltzailea = $stmt->fetch();
?>
```

## 3. CSRF (Cross-Site Request Forgery)

### Arazoa
Erabiltzaileak bere borondatez bestelako ekintzak egin ditzake.

### Konponbidea: CSRF Token-a
```php
<?php
// Token-a sortu
$_SESSION['csrf_token'] = bin2hex(random_bytes(32));

// Formularioan
?>
<input type="hidden" name="csrf_token" value="<?php echo $_SESSION['csrf_token']; ?>">

<?php
// Egiaztapena
if (!isset($_POST['csrf_token']) || $_POST['csrf_token'] !== $_SESSION['csrf_token']) {
    die('CSRF token baliogabea');
}
?>
```

## 4. Segurtasun Hobariak

### Pasahitzen Gordetzea
```php
<?php
// Txarrezkoa
$pasahitza = 'sekretua';
$gordeta = md5($pasahitza); // Ez erabili inoiz

// Ongi
$pasahitz_hashea = password_hash($pasahitza, PASSWORD_DEFAULT);

// Egiaztatu
if (password_verify($sartutako_pasahitza, $gordetako_hashea)) {
    // Pasahitza zuzena
}
?>
```

### Segurtasun-Headerrak
```php
<?php
// X-Content-Type-Options
header('X-Content-Type-Options: nosniff');

// X-Frame-Options
header('X-Frame-Options: DENY');

// Content-Security-Policy
header("Content-Security-Policy: default-src 'self'");
?>
```

## 5. Erabiltzailearen Sarrera Egiaztatzea

Beti egiaztatu erabiltzailearen sarrera eta baimenak:
```php
<?php
session_start();

// Erabiltzailea saioa hasita dagoen egiaztatu
if (!isset($_SESSION['erabiltzailea'])) {
    header('Location: saioa_hasi.php');
    exit;
}

// Erabiltzaileak baimena duen egiaztatu
if ($_SESSION['rola'] !== 'admin') {
    die('Ez duzu baimenik orri hau ikusteko');
}
?>
```

## 6. Fitxategi-igoerak

```php
<?php
$baimendutako_motak = ['image/jpeg', 'image/png'];
$max_tamaina = 5 * 1024 * 1024; // 5MB

if (in_array($_FILES['fitxategia']['type'], $baimendutako_motak) && 
    $_FILES['fitxategia']['size'] <= $max_tamaina) {
    
    $helbidea = 'uploads/' . basename($_FILES['fitxategia']['name']);
    move_uploaded_file($_FILES['fitxategia']['tmp_name'], $helbidea);
}
?>
```
