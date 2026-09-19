#Web 

## 題目

**pathwalker waf**
給了一個網址，點開來：
![[W1-3_web.png|500]]
並附了跟上一題 [[Pathwalker]] 一樣網頁原始碼，但加了一些條件限制
```
  </head>  
    <h1>Pathwalker</h1>  
    <?php
	    if (isset($_GET['page'])) {
	        $lowercaseComponent = strtolower($_GET['page']);
	        $pattern_file = "/^(apple|banana|cappo)/";
	        if (preg_match($pattern_file, $lowercaseComponent)) {
				echo file_get_contents("./page/".$lowercaseComponent.".php");
	        }else{
		        echo "<p>bad hecker detect! </p>";
	        }
	    }      
    ?>
```
三個連結點進去，一樣只有 `Cappo` 出現提示：
![[W1-3_hint.png|413]]
## 解題
1. 題目是 "pathwalker" -> 從路徑目錄切入
2. 提示中寫 flag 在 `/var/www/html/flag.php` -> 根目錄至少在 4 個資料夾之上 -> `?page=` 後面至少接 4 個 `../`，也可以直接塞很多個
	```
	http://chals1:20003/?page=../../../../var/www/html/flag
	```
3. 但網址有條件限制必須以 `apple|banana|cappo` 作為開頭
   ```
   http://chals1:20003/?page=cappo/../../../../../var/www/html/flag
   ```
4. `F12` 找到 flag
   ![[W1-4_flag.png|500]]
5. flag= `CTF{pathwalker_waf_055a7a0e655c15f626a57da3}`