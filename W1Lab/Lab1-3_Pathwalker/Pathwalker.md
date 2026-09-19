#Web 

## 題目

**pathwalker**
給了一個網址，點開來：
![[W1-3_web.png|500]]
並附了網頁原始碼
```
<!DOCTYPE html>  
<html>  
  <head>  
    <title>Pathwalker</title>  
    <link rel="preconnect" href="https://fonts.googleapis.com">  
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>  
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Mono&display=swap" rel="stylesheet">  
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Mono:wght@700&display=swap" rel="stylesheet">  
    <style>  
      body {  
        font-family: 'Noto Sans Mono', monospace;  
      }  
    </style>  
  </head>  
    <h1>Pathwalker</h1>  
    <?php      if (isset($_GET['page'])) {  
        echo file_get_contents("./page/".$_GET['page'].".php");  
      }          ?>  
    <a href='?page=apple'>Apple</a>  
    <a href='?page=banana'>Banana</a>  
    <a href='?page=cappo'>Cappo</a>  
    <hr>  
    <div style="display: inline-block;background-color: rgba(0,0,0,0.1);"><?php highlight_file(__FILE__); ?></div>  
</html>
```
三個連結點進去，只有 `Cappo` 出現提示：
![[W1-3_hint.png|413]]
## 解題
1. 題目是 "pathwalker" -> 從路徑目錄切入
2. 提示中寫 flag 在 `/var/www/html/flag.php` -> 根目錄至少在 4 個資料夾之上 -> `?page=` 後面至少接 4 個 `../`，也可以直接塞很多個
	```
	http://chals1:20002/?page=../../../../var/www/html/flag
	```
3. `F12` 找到 flag
   ![[W1-3_flag.png|500]]
4. flag= `CTF{pathwalker_087dc50666069048282a57be}`