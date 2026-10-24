#Web

## 題目

**Robots**
給了一個網址，點開來：![[W1-1_web.png]]
## 解題
1. 網址後面加上 `robots.txt` 
   ```
   http://chals1:20000/robots.txt
   ```
2. 頁面出現 
   ```
   User-agent: *
	Disallow: /hdw7vtg6cnbKJH/panel.php
   ```
3. 把他輸入網址框
   ```
   http://chals1:20000/hdw7vtg6cnbKJH/panel.php
   ```
   ![[W1-1_rotate.png]]
   可以看到一個一直旋轉的 flag
4. 按 `F12` 找到不會旋轉的 flag
   ```html
   <body>
    <h1>Nothing Here !</h1>
    <p class="rotating-box">CTF{robots_11541e464c511a93b4de845d}</p>
  </body>
   ```
5. flag = `CTF{robots_11541e464c511a93b4de845d}`